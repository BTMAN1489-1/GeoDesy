from django.db import IntegrityError
from rest_framework import serializers
import config
from main_app.models import Session, User, TFA
from main_app.serializers.v1.TFA import TwoFactoryAuthentication
from utils import auth_tools, custom_validators, algorithms, mocks
from utils.context import CurrentContext
from main_app.exceptions import NotFoundAPIError, BadEnterAPIError, PermissionDeniedAPIError


class CreateAuthorizationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    image = serializers.ImageField()

    def create(self, validated_data):
        email = validated_data['email']
        row_password = validated_data['password']
        try:

            user = User.objects.get(email=email)

        except User.DoesNotExist:

            raise NotFoundAPIError(f'Пользователя с email {email} не существует.')

        verified = auth_tools.verify_passwords(user.password, user.salt, row_password)
        if not verified:
            raise BadEnterAPIError('Неправильно введенны данные аутентификации.')

        access_token, refresh_token = Session.create_session(user)
        ctx = CurrentContext()
        ctx.response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "life_expectancy_api_token_in_seconds": config.INTERVAL_API_TOKEN_IN_SECONDS
        }
        return user


class UpdateJWTSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    _payload = None

    def validate_refresh_token(self, refresh_token):
        binary_data, token = custom_validators.validate_token(refresh_token)
        self._payload = algorithms.deserialize_to_dict(binary_data)
        return token

    def create(self, validated_data):
        refresh_token = validated_data['refresh_token']
        try:

            session = Session.objects.get(api_id=self._payload["uuid"])

        except Session.DoesNotExist:
            raise NotFoundAPIError('Указанный токен не существует')

        if not auth_tools.compare_digest(session.refresh_token, refresh_token):
            raise PermissionDeniedAPIError('Недействительный токен обновления')

        access_token, refresh_token = Session.update_session(session)
        ctx = CurrentContext()
        ctx.response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "life_expectancy_api_token_in_seconds": config.INTERVAL_API_TOKEN_IN_SECONDS
        }
        return session


class CreateChangeAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=False)
    password = serializers.CharField(max_length=255, required=False)

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        if not (email or password):
            raise BadEnterAPIError("Необходимо указать новый email или новый пароль.")
        if email is not None:
            custom_validators.check_unique_email(email)

        return attrs

    def create(self, validated_data):
        user = CurrentContext().user
        new_email = validated_data.get('email', None)
        new_password = validated_data.get('password', None)

        if new_email is None:
            new_email = user.email

        password_hash = user.password
        salt = user.salt
        if new_password is not None:
            password_hash, salt = auth_tools.calculate_password_hash(new_password)

        update_user = mocks.User(user.first_name, user.second_name, user.third_name, user.sex, new_email)

        tfa = TwoFactoryAuthentication.create_tfa(user=update_user, event=TFA.Event.ChangeAuth, email=new_email,
                                                  password_hash=password_hash, salt=salt)
        return tfa


class UpdateChangeAuthSerializer(TwoFactoryAuthentication):
    _event = TFA.Event.ChangeAuth

    def create(self, validated_data):
        self.check_tfa(validated_data=validated_data)

        user = CurrentContext().user
        try:
            user.email = self._payload['email']
            user.password = self._payload['password_hash']
            user.salt = self._payload['salt']
            user.save()
        except IntegrityError:
            raise BadEnterAPIError(f"{self._payload['email']} уже занят")

        ctx = CurrentContext()
        ctx.response = {
            "detail": {
                "status": "success",
                "description": "Данные авторизации успешно обновлены."
            }
        }

        return user


class CreateForgottenPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)

    def create(self, validated_data):
        email = validated_data.get('email', None)
        new_password = validated_data.get('password', None)

        try:

            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise NotFoundAPIError(f'Пользователя с email {email} не существует.')
        password_hash, salt = auth_tools.calculate_password_hash(new_password)
        tfa = TwoFactoryAuthentication.create_tfa(user=user, event=TFA.Event.ForgottenPassword,
                                                  password_hash=password_hash, salt=salt, email=email)
        return tfa


class UpdateForgottenPasswordSerializer(TwoFactoryAuthentication):
    _event = TFA.Event.ForgottenPassword

    def create(self, validated_data):
        self.check_tfa(validated_data=validated_data)
        email = self._payload['email']

        try:

            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise NotFoundAPIError(f'Пользователя с email {email} не существует.')
        user.password = self._payload['password_hash']
        user.salt = self._payload['salt']
        user.save()

        ctx = CurrentContext()
        ctx.response = {
            "detail": {
                "status": "success",
                "description": "Пароль успешно обновлен."
            }
        }

        return user
