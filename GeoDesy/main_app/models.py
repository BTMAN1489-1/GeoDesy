import uuid
from datetime import datetime, timedelta
from django.db import models
from utils.auth_tools import create_jwt_tokens
import config


class CountMixin:
    @classmethod
    def count_rows(cls):
        count = cls.objects.count()
        return count


class User(models.Model):
    class Sex(models.TextChoices):
        MALE = 'male', 'Мужской'
        FEMALE = 'female', 'Женский'

    first_name = models.CharField(max_length=255, verbose_name='Имя')
    second_name = models.CharField(max_length=255, verbose_name='Фамилия')
    third_name = models.CharField(max_length=255, verbose_name='Отчество')
    sex = models.TextField(choices=Sex.choices, verbose_name='Пол')

    email = models.EmailField(verbose_name='Email', unique=True)

    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')

    password = models.CharField()

    salt = models.CharField()

    def __str__(self):
        return f"{self.second_name}  {self.first_name} {self.third_name}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Card(models.Model, CountMixin):
    class Status(models.TextChoices):
        SUCCESS = 'success', 'Успешно'
        DENIED = 'denied', 'Отказано'
        PENDING = 'pending', 'В процессе проверки'
        SENDING = 'sending', 'Отправлено'

    status = models.TextField(choices=Status.choices)
    date_creation = models.DateTimeField(auto_now_add=True)
    executor = models.ForeignKey('User', on_delete=models.PROTECT, related_name='exec_cards')
    inspector = models.ForeignKey('User', null=True, on_delete=models.PROTECT, related_name='inspect_cards')
    coordinates = models.ForeignKey('GeoPoint', on_delete=models.PROTECT, related_name='cards')
    description = models.JSONField()


    class Meta:
        verbose_name = 'карточка'
        verbose_name_plural = 'карточки'

    def __str__(self):
        return f'Card({self.date_creation})::Status({self.status})'


class FederalDistrict(models.Model):
    name = models.TextField(unique=True)


class FederalSubject(models.Model):
    subject_code = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)
    district = models.ForeignKey('FederalDistrict', on_delete=models.PROTECT, related_name='subjects')


class GeoPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    subject = models.ForeignKey('FederalSubject', on_delete=models.PROTECT, related_name='geo_points')


class TFA(models.Model):
    class Event(models.TextChoices):
        Registration = "Registration", "Регистрация"
        Authorization = "Authorization", "Авторизация"
        ChangeAuth = "ChangeAuth", "Изменение данных авторизация"
        ForgottenPassword = "ForgottenPassword", "Восстановление пароля"

    tfa_id = models.CharField(primary_key=True)
    confirm_code = models.CharField()
    expired_datetime_code = models.DateTimeField()


class Session(models.Model):
    api_id = models.UUIDField(primary_key=True)
    update_session_datetime = models.DateTimeField(auto_now=True)
    refresh_token = models.CharField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sessions')

    @staticmethod
    def create_session(user):
        api_id = uuid.uuid4().hex
        expiration_datetime = datetime.utcnow() + timedelta(seconds=config.INTERVAL_API_TOKEN_IN_SECONDS)
        access_token, refresh_token = create_jwt_tokens(api_id, expiration_datetime)
        Session.objects.create(api_id=api_id, refresh_token=refresh_token, user=user)
        return access_token, refresh_token

    @staticmethod
    def update_session(session):
        expiration_datetime = datetime.utcnow() + timedelta(seconds=config.INTERVAL_API_TOKEN_IN_SECONDS)
        access_token, refresh_token = create_jwt_tokens(session.api_id.hex, expiration_datetime)
        session.refresh_token = refresh_token
        session.save()
        return access_token, refresh_token
