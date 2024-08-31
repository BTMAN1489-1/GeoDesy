from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from rest_framework import serializers
import config
from main_app.models import Session, User, TFA
from main_app.serializers.v1.TFA import TwoFactoryAuthentication
from utils import auth_tools, custom_validators, algorithms, mocks
from utils.context import CurrentContext
from main_app.exceptions import NotFoundAPIError, BadEnterAPIError

__all__ = (
    "CreateAuthorizationSerializer", "UpdateJWTSerializer", "CreateChangeAuthSerializer",
    "CreateChangeAuthSerializer", "UpdateChangeAuthSerializer", "CreateForgottenPasswordSerializer",
    "UpdateForgottenPasswordSerializer"
)


class CreateAuthorizationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)

    def create(self, validated_data):
        email = validated_data['email']
        row_password = validated_data['password']
        try:

            user = User.objects.get(email=email)

        except User.DoesNotExist:

            raise NotFoundAPIError(f'Пользователя с email {email} не существует.')

        verified = user.check_password(row_password)
        if not verified:
            raise BadEnterAPIError('Неправильно введенны данные аутентификации.')

        session = Session.objects.create(user)
        expiration_datetime = datetime.utcnow() + timedelta(seconds=config.INTERVAL_API_TOKEN_IN_SECONDS)
        access_token, refresh_token = auth_tools.create_jwt_tokens(session.api_id.hex, expiration_datetime)
        ctx = CurrentContext()
        ctx.response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "life_expectancy_api_token_in_seconds": config.INTERVAL_API_TOKEN_IN_SECONDS
        }
        return user


class UpdateJWTSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        binary_data = custom_validators.validate_token(attrs["refresh_token"])
        payload = algorithms.deserialize_to_dict(binary_data)
        attrs["payload"] = payload
        return attrs

    def create(self, validated_data):
        payload = validated_data['payload']
        try:

            session = Session.objects.get(api_id=payload["uuid"])

        except Session.DoesNotExist:
            raise NotFoundAPIError('Указанный токен не существует')

        expiration_datetime = datetime.utcnow() + timedelta(seconds=config.INTERVAL_API_TOKEN_IN_SECONDS)
        access_token, refresh_token = auth_tools.create_jwt_tokens(session.api_id.hex, expiration_datetime)
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

        if new_password is not None:
            password_hash = make_password(new_password)

        update_user = mocks.User(user.first_name, user.second_name, user.third_name, user.sex, new_email)

        tfa = TwoFactoryAuthentication.create_tfa(user=update_user, event=TFA.Event.ChangeAuth, email=new_email,
                                                  password_hash=password_hash)
        return tfa


class UpdateChangeAuthSerializer(TwoFactoryAuthentication):
    _event = TFA.Event.ChangeAuth

    def create(self, validated_data):
        payload = self.check_tfa(validated_data=validated_data)

        user = CurrentContext().user
        try:
            user.email = payload['email']
            user.password = payload['password_hash']
            user.save()
        except IntegrityError:
            raise BadEnterAPIError(f"{payload['email']} уже занят")

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
        password_hash = make_password(new_password)
        tfa = TwoFactoryAuthentication.create_tfa(user=user, event=TFA.Event.ForgottenPassword,
                                                  password_hash=password_hash, email=email)
        return tfa


class UpdateForgottenPasswordSerializer(TwoFactoryAuthentication):
    _event = TFA.Event.ForgottenPassword

    def create(self, validated_data):
        payload = self.check_tfa(validated_data=validated_data)
        email = payload['email']

        try:

            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise NotFoundAPIError(f'Пользователя с email {email} не существует.')
        user.password = payload['password_hash']
        user.save()

        return user
