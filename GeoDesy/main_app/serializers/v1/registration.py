from rest_framework import serializers
import config
from .TFA import TwoFactoryAuthentication
from main_app.models import Session, User, TFA
from utils.custom_validators import validate_russian_text, check_unique_email
from utils.auth_tools import calculate_password_hash
from django.db import IntegrityError
from main_app.exceptions import BadEnterAPIError
from utils.context import CurrentContext
from utils import mocks


class CreateRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255, validators=(validate_russian_text,))
    second_name = serializers.CharField(max_length=255, validators=(validate_russian_text,))
    third_name = serializers.CharField(max_length=255, validators=(validate_russian_text,))
    sex = serializers.ChoiceField(choices=User.Sex.choices)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)

    def validate_email(self, email):
        check_unique_email(email)
        return email

    def create(self, validated_data):
        password_hash, salt = calculate_password_hash(validated_data['password'])
        user = mocks.User(email=validated_data['email'], first_name=validated_data['first_name'],
                          second_name=validated_data['second_name'],
                          third_name=validated_data['third_name'],
                          sex=validated_data['sex'])

        tfa = TwoFactoryAuthentication.create_tfa(event=TFA.Event.Registration, user=user,
                                                  email=user.email,
                                                  password_hash=password_hash, salt=salt,
                                                  first_name=user.first_name,
                                                  second_name=user.second_name,
                                                  third_name=user.third_name,
                                                  sex=user.sex)
        return tfa


class UpdateRegistrationSerializer(TwoFactoryAuthentication):
    _event = TFA.Event.Registration

    def create(self, validated_data):
        self.check_tfa(validated_data=validated_data)

        try:
            user = User.objects.create(
                first_name=self._payload['first_name'],
                second_name=self._payload['second_name'],
                third_name=self._payload['third_name'],
                sex=self._payload['sex'],
                email=self._payload['email'],
                password=self._payload['password_hash'],
                salt=self._payload['salt'],
            )
        except IntegrityError:
            raise BadEnterAPIError(f"Потльзователь с почтой {self._payload['email']} уже существует.")

        access_token, refresh_token = Session.create_session(user)
        ctx = CurrentContext()
        ctx.response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expiration_access_token_in_seconds": config.INTERVAL_API_TOKEN_IN_SECONDS
        }
        return user
