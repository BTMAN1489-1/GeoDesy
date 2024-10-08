__all__ = (
    "displayed_Card_fields", "displayed_GeoPoint_fields", "displayed_Photo_fields", "owners", "sorted_fields",
    "mapper_related_GeoPoint_fields", "mapper_related_Federal_fields", "mapper_related_fields",
    "reverse_mapper_related_fields", "displayed_fields", "CardData", "FEDERAL_SUBJECTS_DICT", "FEDERAL_SUBJECTS_NAMES",
    "FEDERAL_SUBJECTS_CODES"
)


class CardData:
    def __init__(self, obj_model):
        self.card = obj_model
        self.coordinates = obj_model.coordinates
        self.executor = obj_model.executor
        self.inspector = obj_model.inspector
        self.photos = obj_model.photos.all()


displayed_Card_fields = {"status", "execute_date", "identification_pillar",
                         "monolith_one", "monolith_two", "monolith_three_and_four", "sign_height_above_ground_level",
                         "sign_height",
                         "outdoor_sign", "ORP_one", "ORP_two", "trench", "satellite_surveillance", "type_of_sign",
                         "point_index", "name_point", "year_of_laying", "type_of_center", "height_above_sea_level",
                         "trapezoids", "datetime_creation", "datetime_inspection"}

displayed_GeoPoint_fields = {"latitude", "longitude", "federal_subject", "federal_district"}
displayed_Photo_fields = {"photos"}
owners = {"executor", "inspector"}

sorted_fields = {"datetime_creation", "datetime_inspection"}

mapper_related_GeoPoint_fields = {"latitude": "coordinates__latitude", "longitude": "coordinates__longitude"}

mapper_related_Federal_fields = {"federal_subject": "coordinates__subject__name",
                                 "federal_district": "coordinates__subject__district__name"
                                 }

mapper_related_fields = mapper_related_Federal_fields | mapper_related_GeoPoint_fields

reverse_mapper_related_fields = {"latitude": "coordinates__latitude", "longitude": "coordinates__longitude",
                                 "federal_subject": "coordinates__subject__name",
                                 "federal_district": "coordinates__subject__district__name"
                                 }

displayed_fields = displayed_Card_fields | displayed_GeoPoint_fields | owners | displayed_Photo_fields

FEDERAL_SUBJECTS_DICT = {'Белгородская область': 31, 'Брянская область': 32, 'Владимирская область': 33,
                         'Воронежская область': 36,
                         'Ивановская область': 37, 'Калужская область': 40, 'Костромская область': 44,
                         'Курская область': 46,
                         'Липецкая область': 48, 'Московская область': 50, 'Орловская область': 57,
                         'Рязанская область': 62,
                         'Смоленская область': 67, 'Тамбовская область': 68, 'Тверская область': 69,
                         'Тульская область': 71,
                         'Ярославская область': 76, 'г. Москва': 77, 'Республика Карелия': 10, 'Республика Коми': 11,
                         'Архангельская область': 29, 'Ненецкий автономный округ': 83, 'Вологодская область': 35,
                         'Калининградская область': 39,
                         'Ленинградская область': 47, 'Мурманская область': 51, 'Новгородская область': 53,
                         'Псковская область': 60,
                         'г. Санкт-Петербург': 78, 'Республика Адыгея': 1, 'Республика Калмыкия': 8,
                         'Краснодарский край': 23,
                         'Астраханская область': 30, 'Волгоградская область': 34, 'Ростовская область': 61,
                         'Республика Дагестан': 5,
                         'Республика Ингушетия': 6, 'Кабардино-Балкарская Республика': 7,
                         'Карачаево-Черкесская Республика': 9,
                         'Республика Северная Осетия-Алания': 15, 'Чеченская Республика': 20, 'Ставропольский край': 26,
                         'Республика Башкортостан': 2, 'Республика Марий Эл': 12, 'Республика Мордовия': 13,
                         'Республика Татарстан': 16,
                         'Удмуртская Республика': 18, 'Чувашская Республика': 21, 'Пермский край': 59,
                         'Кировская область': 43,
                         'Нижегородская область': 52, 'Оренбургская область': 56, 'Пензенская область': 58,
                         'Самарская область': 63,
                         'Саратовская область': 64, 'Ульяновская область': 73, 'Курганская область': 45,
                         'Свердловская область': 66,
                         'Тюменская область': 72, 'Ханты-Мансийский автономный округ': 86,
                         'Ямало-Ненецкий автономный округ': 89,
                         'Челябинская область': 74, 'Республика Алтай': 4, 'Республика Бурятия': 3,
                         'Республика Тыва': 17,
                         'Республика Хакасия': 19, 'Алтайский край': 22, 'Забайкальский край': 75,
                         'Красноярский край': 24,
                         'Иркутская область': 38, 'Кемеровская область': 42, 'Новосибирская область': 54,
                         'Омская область': 55,
                         'Томская область': 70, 'Республика Саха (Якутия)': 14, 'Камчатский край': 41,
                         'Приморский край': 25,
                         'Хабаровский край': 27, 'Амурская область': 28, 'Магаданская область': 49,
                         'Сахалинская область': 65,
                         'Еврейская автономная область': 79, 'Чукотский автономный округ': 87, 'г. Севастополь': 92,
                         'Республика Крым': 91,
                         'Иные территории, включая город и космодром Байконур': 99}

FEDERAL_SUBJECTS_NAMES = tuple(FEDERAL_SUBJECTS_DICT.keys())
FEDERAL_SUBJECTS_CODES = tuple(FEDERAL_SUBJECTS_DICT.values())