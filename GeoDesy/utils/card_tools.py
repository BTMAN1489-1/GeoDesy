import enum
from django.db import models

displayed_Card_fields = {"status", "execute_date", "identification_pillar",
                         "monolith_one", "monolith_two", "monolith_three_and_four", "sign_height_above_ground_level",
                         "outdoor_sign", "ORP_one", "ORP_two", "trench", "satellite_surveillance", "type_of_sign",
                         "point_index", "name_point", "year_of_laying", "type_of_center", "height_above_sea_level",
                         "trapezoids", "datetime_creation", "datetime_inspection"}

displayed_GeoPoint_fields = {"latitude", "longitude", "federal_subject", "federal_district"}
displayed_Photo_fields = {"photos"}
owners = {"executor", "inspector"}
displayed_fields = displayed_Card_fields | displayed_GeoPoint_fields | owners | displayed_Photo_fields

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


def to_representation(user, card, allow_fields):
    if allow_fields is None:
        allow_fields = displayed_fields
    else:
        allow_fields = set(allow_fields)

    coordinates = {}
    result = {"card_uuid": card.card_uuid}
    card_fields = displayed_Card_fields
    geo_fields = displayed_GeoPoint_fields
    owner_fields = owners
    for field in allow_fields:
        if field in card_fields:
            result[field] = getattr(card, field)
        elif field in owner_fields:
            owner = getattr(card, field)
            to_dict = getattr(owner, "to_dict", lambda x: None)
            result[field] = to_dict(user.is_staff)

        elif field in geo_fields:
            geo_point = getattr(card, "coordinates")
            coordinates[field] = getattr(geo_point, field)

        else:
            result[field] = getattr(card, "photos_url")

    if coordinates:
        result["coordinates"] = coordinates

    return result


class Item:
    def __init__(self, value, label, **sub_items):
        self._value = value
        self._label = label
        self._sub_items = sub_items

    @property
    def sub_items(self):
        return self._sub_items

    @property
    def value(self):
        return self._value

    @property
    def label(self):
        return self._label

    def __str__(self):
        return f"{self._label}"

    def __repr__(self):
        return f"'{self._value}'"

    @property
    def item(self):
        return self._value, self._label


class ArrayItem:
    def __init__(self, label: str, *items: Item):
        self._label = label
        new_items = self._items = dict((item.value, item)for item in items)
        self._values = tuple(new_items.keys())
        self._labels = tuple(new_items.values())

    def __str__(self):
        return f"{self._items}"

    def __repr__(self):
        return f"{repr(self._items)}"

    @property
    def label(self):
        return self._label

    @property
    def labels(self):
        return self._labels

    @property
    def values(self):
        return self._values

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item):
        if isinstance(item, Item):
            return item in self._items
        else:
            return item in self._values

    def __getitem__(self, item):
        return self._items[item]

    def get(self, item, default=None):
        return self._items.get(item, default)


class MetaChoice(enum.EnumType):
    @property
    def choices(cls):
        result = list()
        for elem in cls:
            choice = elem.value
            result.append(choice.item)

        return result

    def __getitem__(cls, item):
        return vars(cls)[item]

    def get(cls,  item, default=None):
        return vars(cls).get(item, default)


class Choice(enum.Enum, metaclass=MetaChoice):
    def __str__(self):
        return f"{self.value}"

    @property
    def sub_choices(self):
        return self.value.sub_items


class TypeSignChoice(Choice):
    signal = Item("signal", "сигнал",
                  type=ArrayItem("тип",

                                 Item("simple", "простой"),
                                 Item("complex", "сложный"))
                  )

    pyramid = Item("pyramid", "пирамида",
                   material=ArrayItem("материал",
                                      Item("wood", "деревянный"),
                                      Item("metalic", "металлический")),
                   geometry=ArrayItem("геометрия",
                                      Item("trihedron", "трехгранная"),
                                      Item("tetrahedron", "четырехгранная"))
                   )

    tripod = Item("tripod", "штатив",
                  material=ArrayItem("материал",
                                     Item("wood", "деревянный"),
                                     Item("metalic", "металлический")),
                  geometry=ArrayItem("геометрия",
                                     Item("trihedron", "трехгранная"),
                                     Item("tetrahedron", "четырехгранная"))
                  )

    tur = Item("tur", "тур",
               pillar=ArrayItem("столб",
                                Item("concrete", "бетонный"),
                                Item("stone", "каменный"),
                                Item("brick", "кирпичный"))
               )

    no_sign = Item("no_sign", "знак отсутствует")


class DetectedPropertyChoice(models.TextChoices):
    DETECTED = "detected", "обнаружен"
    UNDETECTED = "undetected", "не обнаружен"


class SavingPropertyChoice(models.TextChoices):
    SAVED = "saved", "сохранился"
    UNSAVED = "unsaved", "не сохранился"


class CoveringPropertyChoice(models.TextChoices):
    COVERED = "covered", "не вскрывался"
    UNCOVERED = "uncovered", "вскрывался"


class ReadingPropertyChoice(models.TextChoices):
    READABLE = "readable", "читается"
    UNREADABLE = "unreadable", "не читается"


class PossiblePropertyChoice(models.TextChoices):
    POSSIBLE = "possible", "возможно"
    CONDITIONALLY_POSSIBLE = "conditionally_possible", "условно возможно"
    IMPOSSIBLE = "impossible", "невозможно"


class MetaStatusChoice(models.enums.ChoicesType):

    @classmethod
    def _create_new_class(metacls, name, items, filter_names):
        bases = (models.TextChoices,)
        attrs = metacls.__prepare__(name, bases)
        for key, value in items:
            if key in filter_names:
                attrs[key] = value
        new_class = metacls(name, bases, attrs)
        return new_class

    @staticmethod
    def _unique_choices(names, values):
        unique_filter = set()
        result = []
        for name in names:
            value = values.pop(0)
            if name not in unique_filter:
                result.append((name, value))
            unique_filter.add(name)

        return result

    def _result_operation(cls, other, new_class_name, filter_names):
        names = cls.names + other.names
        values = cls.choices + other.choices
        items = cls._unique_choices(names, values)
        return cls._create_new_class(new_class_name, items, filter_names)

    def __or__(cls, other):
        new_class_name = f"{cls.__name__}Or{other.__name__}"
        filter_names = set(cls.names) | set(other.names)
        new_class = cls._result_operation(other, new_class_name, filter_names)

        return new_class

    def __and__(cls, other):
        new_class_name = f"{cls.__name__}And{other.__name__}"
        filter_names = set(cls.names) & set(other.names)
        new_class = cls._result_operation(other, new_class_name, filter_names)

        return new_class

    def __xor__(cls, other):
        new_class_name = f"{cls.__name__}Without{other.__name__}"
        filter_names = set(cls.names).difference(set(other.names))
        new_class = cls._result_operation(other, new_class_name, filter_names)

        return new_class
