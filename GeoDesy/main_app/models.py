from django.db import models
from main_app.db import *
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from utils.custom_validators import validate_russian_text
from utils.card_tools import CardChoices, printable_coordinates
from django.conf import settings

__all__ = (
    "User", "FederalDistrict", "FederalSubject", "GeoPoint", "TFA", "Session", "Photo", "Card"
)


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

    objects = UserManager()

    @property
    def full_name(self):
        return " ".join(map(str.capitalize, (self.second_name, self.first_name, self.third_name)))

    @property
    def get_user_info(self):
        return {"full_name": self.full_name, "email": self.email}

    def to_dict(self, is_staff=False):
        d = {"first_name": self.first_name, "second_name": self.second_name, "third_name": self.third_name}
        if is_staff:
            d["email"] = self.email

        return d

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class FederalDistrict(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class FederalSubject(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    name = models.TextField(unique=True, verbose_name="Субъект РФ")
    district = models.ForeignKey('FederalDistrict', on_delete=models.PROTECT, related_name='subjects', verbose_name="Федеральный округ РФ")

    def __str__(self):
        return self.name


class GeoPoint(models.Model):
    guid = models.UUIDField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    subject = models.ForeignKey('FederalSubject', on_delete=models.PROTECT, related_name='geo_points', verbose_name="Субъект РФ")

    objects = MapQuerySet.as_manager()

    class Meta:
        verbose_name = 'координаты'
        verbose_name_plural = 'координаты'
        ordering = ("latitude", "longitude")
        constraints = (models.UniqueConstraint(fields=('latitude', 'longitude'), name='unique_coordinates'),)

    @property
    def federal_subject(self):
        return self.subject.name

    @property
    def federal_district(self):
        return self.subject.district.name

    @property
    def printable_coordinates(self):
        return printable_coordinates(self)

    def __str__(self):
        return "     ".join(self.printable_coordinates)


class TFA(models.Model):
    class Event(models.TextChoices):
        Registration = "Registration", "Регистрация"
        Authorization = "Authorization", "Авторизация"
        ChangeAuth = "ChangeAuth", "Изменение данных авторизация"
        ForgottenPassword = "ForgottenPassword", "Восстановление пароля"

    tfa_id = models.UUIDField(primary_key=True)
    confirm_code = models.CharField()
    expired_datetime_code = models.DateTimeField()

    objects = TFAQuerySet.as_manager()


class Session(models.Model):
    api_id = models.UUIDField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sessions')

    objects = SessionQuerySet.as_manager()


class Photo(models.Model):
    path = models.ImageField(upload_to="photos/%Y/%m/%d")
    card_ref = models.ForeignKey("Card", on_delete=models.PROTECT, related_name='photos')

    @property
    def absolute_path(self):
        return settings.MEDIA_ROOT / self.path.name

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'


class Card(models.Model):
    class SuccessChoice(CardChoices):
        SUCCESS = 'success', 'Принято'

    class DeniedChoice(CardChoices):
        DENIED = 'denied', 'Отвергнуто'

    class PendingChoice(CardChoices):
        PENDING = 'pending', 'В процессе проверки'

    class SendingChoice(CardChoices):
        SENDING = 'sending', 'Отправлено'

    StatusChoice = PendingChoice | SendingChoice | SuccessChoice | DeniedChoice
    StatusChoiceWithOutSending = StatusChoice ^ SendingChoice

    card_uuid = models.UUIDField(primary_key=True)
    status = models.TextField(choices=StatusChoice.choices, verbose_name="Статус")
    datetime_creation = models.DateTimeField(auto_now_add=True, verbose_name="Время создания (UTC-формат)")
    execute_date = models.DateField(verbose_name="Дата проведения работ")
    datetime_inspection = models.DateTimeField(null=True, default=None, verbose_name="Время последней проверки (UTC-формат)")
    executor = models.ForeignKey('User', on_delete=models.PROTECT, related_name='exec_cards')
    inspector = models.ForeignKey('User', null=True, on_delete=models.PROTECT, related_name='inspect_cards')
    coordinates = models.ForeignKey('GeoPoint', on_delete=models.PROTECT, related_name='cards', verbose_name="Координаты")

    identification_pillar = models.JSONField(verbose_name="Опознавательный столб")

    monolith_one = models.JSONField(verbose_name="Монолит I")
    monolith_two = models.JSONField(verbose_name="Монолит II")
    monolith_three_and_four = models.JSONField(verbose_name="Монолиты III и IV")
    sign_height_above_ground_level = models.FloatField(verbose_name="Высота верхней марки")
    sign_height = models.FloatField(verbose_name="Высота знака")
    outdoor_sign = models.JSONField(verbose_name="Наружный знак")

    ORP_one = models.JSONField(verbose_name="ОРП I")
    ORP_two = models.JSONField(verbose_name="ОРП II")

    trench = models.JSONField(verbose_name="Окопка")

    satellite_surveillance = models.JSONField(verbose_name="Спутниковое наблюдение")

    type_of_sign = models.JSONField(verbose_name="Тип знака")

    point_index = models.CharField(null=True, default=None, blank=True, verbose_name="№ по каталогу/индекс пункта")
    name_point = models.CharField(null=True, default=None, blank=True, verbose_name="Название пункта, класс, № марки")
    year_of_laying = models.IntegerField(null=True, default=None, verbose_name="Год закладки")
    type_of_center = models.CharField(null=True, default=None, blank=True, verbose_name="Тип центра")
    height_above_sea_level = models.FloatField(null=True, default=None, blank=True,
                                               verbose_name="Высота над уровнем моря")
    trapezoids = models.CharField(null=True, default=None, blank=True, verbose_name="Трапеции")

    objects = CardQueryset.as_manager()

    class Meta:
        verbose_name = 'карточка пункта ГГС'
        verbose_name_plural = 'карточки пунктов ГГС'

    @property
    def photos_url(self):
        return [photo.path.url for photo in self.photos.all()]

    @property
    def print_status(self):
        return dict(self.StatusChoice.choices).get(self.status, "")

    def __str__(self):
        return f'Карточка/{self.pk}'
