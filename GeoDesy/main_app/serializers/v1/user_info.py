from rest_framework import serializers
from main_app.models import User
from utils.custom_validators import validate_russian_text

__all__ = (
    "UserInfoSerializer",
)


class UserInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(validators=(validate_russian_text,))
    second_name = serializers.CharField(validators=(validate_russian_text,))
    third_name = serializers.CharField(validators=(validate_russian_text,))

    class Meta:
        model = User
        fields = ('first_name', 'second_name', 'third_name', 'sex', 'email', 'is_staff')
        read_only_fields = ('email', 'is_staff')
