import uuid
from datetime import datetime, timedelta
from rest_framework import serializers
import config
from main_app.models import TFA
from utils import auth_tools, algorithms, handlers, custom_validators
from main_app.exceptions import NotFoundAPIError, AuthenticationFailedAPIError
from utils.context import CurrentContext


class TwoFactoryAuthentication(serializers.Serializer):
    tfa_token = serializers.CharField()
    confirm_code = serializers.CharField()

    _event = None
    _payload = None

    @classmethod
    def verify_event(cls, event: str):
        if event != cls._event:
            raise AuthenticationFailedAPIError("Неверный TFA токен.")

    def validate_tfa_token(self, tfa_token: str):
        binary_data, token = custom_validators.validate_token(tfa_token)
        self._payload = algorithms.deserialize_to_dict(binary_data)
        return token

    @classmethod
    def create_tfa(cls, /, event, user, **kwargs):
        confirm_code = auth_tools.create_confirm_code()
        tfa_id = uuid.uuid4().hex
        expired_datetime_code = datetime.utcnow() + timedelta(seconds=config.INTERVAL_CONFIRM_CODE_IN_SECONDS)

        data = {"uuid": tfa_id, "event": event}
        data.update(kwargs)
        binary_data = algorithms.serialize_to_json(data)
        tfa_token = auth_tools.create_token(binary_data)
        ctx = CurrentContext()
        ctx.response = {
            "tfa_token": tfa_token,
            "expiration_confirm_code_in_seconds": config.INTERVAL_CONFIRM_CODE_IN_SECONDS
        }
        message_handler = handlers.MessageHandler(user)
        message_handler.send_confirm_code(confirm_code)

        return TFA.objects.create(
            tfa_id=tfa_id,
            confirm_code=confirm_code,
            expired_datetime_code=expired_datetime_code
        )

    def check_tfa(self, validated_data: dict):
        current_datetime = datetime.utcnow()

        self.verify_event(self._payload['event'])

        try:
            tfa = TFA.objects.get(tfa_id=self._payload["uuid"])
        except TFA.DoesNotExist:
            raise NotFoundAPIError("Незарегистрированый TFA токен")

        if tfa.expired_datetime_code < current_datetime:
            raise AuthenticationFailedAPIError("Отправленный код подверждения просрочен")

        if tfa.confirm_code != validated_data['confirm_code']:
            raise AuthenticationFailedAPIError("Неверный код подверждения")

        tfa.delete()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
