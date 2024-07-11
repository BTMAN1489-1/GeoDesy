from rest_framework import serializers


class JWTSuccessResponse(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    expiration_access_token_in_seconds = serializers.IntegerField()

