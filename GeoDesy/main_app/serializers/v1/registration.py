from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
import config
from .TFA import TwoFactoryAuthentication
from main_app.models import Session, User, TFA
from utils.custom_validators import validate_russian_text, check_unique_email
from utils.auth_tools import create_jwt_tokens
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
        row_password = validated_data["password"]
        password_hash = make_password(row_password)
        user = mocks.User(email=validated_data['email'], first_name=validated_data['first_name'],
                          second_name=validated_data['second_name'],
                          third_name=validated_data['third_name'],
                          sex=validated_data['sex'])

        tfa = TwoFactoryAuthentication.create_tfa(event=TFA.Event.Registration, user=user,
                                                  email=user.email,
                                                  password_hash=password_hash,
                                                  first_name=user.first_name,
                                                  second_name=user.second_name,
                                                  third_name=user.third_name,
                                                  sex=user.sex)
        return tfa


class UpdateRegistrationSerializer(TwoFactoryAuthentication):
    _event = TFA.Event.Registration

    def create(self, validated_data):
        payload = self.check_tfa(validated_data=validated_data)

        try:
            user = User.objects.create(
                first_name=payload['first_name'],
                second_name=payload['second_name'],
                third_name=payload['third_name'],
                sex=payload['sex'],
                email=payload['email'],
                password=payload['password_hash']
            )
        except IntegrityError:
            raise BadEnterAPIError(f"Потльзователь с почтой {payload['email']} уже существует.")

        session = Session.objects.create(user)
        expiration_datetime = datetime.utcnow() + timedelta(seconds=config.INTERVAL_API_TOKEN_IN_SECONDS)
        access_token, refresh_token = create_jwt_tokens(session.api_id.hex, expiration_datetime)
        ctx = CurrentContext()
        ctx.response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expiration_access_token_in_seconds": config.INTERVAL_API_TOKEN_IN_SECONDS
        }
        return user
