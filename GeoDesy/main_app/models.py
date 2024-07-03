from django.db import models
from main_app.db import managers
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from utils.custom_validators import validate_russian_text


class User(AbstractBaseUser, PermissionsMixin):
    class Sex(models.TextChoices):
        MALE = 'male', 'Мужской'
        FEMALE = 'female', 'Женский'
        UNKNOWN = 'unknown', 'Другое'

    first_name = models.CharField(max_length=255, verbose_name='Имя', validators=(validate_russian_text,))
    second_name = models.CharField(max_length=255, verbose_name='Фамилия', validators=(validate_russian_text,))
    third_name = models.CharField(max_length=255, verbose_name='Отчество', validators=(validate_russian_text,))
    sex = models.TextField(choices=Sex.choices, verbose_name='Пол', validators=(validate_russian_text,))

    email = models.EmailField(verbose_name='Email', unique=True,
                              error_messages={
                                  "unique": "Пользователь с таким email уже существует."}
                              )
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False, verbose_name='Статус сотрудника')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    USERNAME_FIELD = "email"

    objects = managers.UserManager()

    def to_dict(self, is_staff=False):
        d = {"first_name": self.first_name, "second_name": self.second_name, "third_name":self.third_name}
        if is_staff:
            d["email"] = self.email

        return d

    def __str__(self):
        return f"{self.second_name.capitalize()}  {self.first_name.capitalize()} {self.third_name.capitalize()}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class FederalDistrict(models.Model):
    name = models.TextField(unique=True)


class FederalSubject(models.Model):
    subject_code = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)
    district = models.ForeignKey('FederalDistrict', on_delete=models.PROTECT, related_name='subjects')


class GeoPoint(models.Model):
    guid = models.UUIDField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    subject = models.ForeignKey('FederalSubject', on_delete=models.PROTECT, related_name='geo_points')

    objects = managers.MapQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('latitude', 'longitude'), name='unique_coordinates'),
        ]

    @property
    def federal_subject(self):
        return self.subject.name

    @property
    def federal_district(self):
        return self.subject.district.name

    def __str__(self):
        return f"GeoPoint([{self.latitude}, {self.longitude}], {self.guid})"


class TFA(models.Model):
    class Event(models.TextChoices):
        Registration = "Registration", "Регистрация"
        Authorization = "Authorization", "Авторизация"
        ChangeAuth = "ChangeAuth", "Изменение данных авторизация"
        ForgottenPassword = "ForgottenPassword", "Восстановление пароля"

    tfa_id = models.UUIDField(primary_key=True)
    confirm_code = models.CharField()
    expired_datetime_code = models.DateTimeField()

    objects = managers.TFAQuerySet.as_manager()


class Session(models.Model):
    api_id = models.UUIDField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sessions')

    objects = managers.SessionQuerySet.as_manager()


class Photo(models.Model):
    path = models.ImageField(upload_to="photos/%Y/%m/%d")
    card_ref = models.ForeignKey("Card", on_delete=models.PROTECT, related_name='photos')

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'


class Card(models.Model):
    class StatusChoice(models.TextChoices):
        SUCCESS = 'success', 'Успешно'
        DENIED = 'denied', 'Отказано'
        PENDING = 'pending', 'В процессе проверки'
        SENDING = 'sending', 'Отправлено'

    card_uuid = models.UUIDField(primary_key=True)
    status = models.TextField(choices=StatusChoice.choices)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    execute_date = models.DateField()
    datetime_inspection = models.DateTimeField(null=True, default=None)
    executor = models.ForeignKey('User', on_delete=models.PROTECT, related_name='exec_cards')
    inspector = models.ForeignKey('User', null=True, on_delete=models.PROTECT, related_name='inspect_cards')
    coordinates = models.ForeignKey('GeoPoint', on_delete=models.PROTECT, related_name='cards')

    identification_pillar = models.JSONField()

    monolith_one = models.JSONField()
    monolith_two = models.JSONField()
    monolith_three_and_four = models.JSONField()
    sign_height_above_ground_level = models.FloatField()
    outdoor_sign = models.JSONField()

    ORP_one = models.JSONField()
    ORP_two = models.JSONField()

    trench = models.JSONField()

    satellite_surveillance = models.JSONField()

    type_of_sign = models.JSONField()

    point_index = models.CharField(null=True, default=None)
    name_point = models.CharField(null=True, default=None)
    year_of_laying = models.IntegerField(null=True, default=None)
    type_of_center = models.CharField(null=True, default=None)
    height_above_sea_level = models.FloatField(null=True, default=None)
    trapezoids = models.CharField(null=True, default=None)

    objects = managers.CardQueryset.as_manager()

    class Meta:
        verbose_name = 'карточка'
        verbose_name_plural = 'карточки'

    @property
    def photos_url(self):
        return [photo.path.url for photo in self.photos.all()]

    def __str__(self):
        return f'Card({self.execute_date})::Status({self.status})'
