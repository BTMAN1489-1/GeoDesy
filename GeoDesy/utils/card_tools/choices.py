import enum
from django.db import models

__all__ = ("TypeSignChoice", "CardChoices", "DetectedPropertyChoice", "SavingPropertyChoice",
           "CoveringPropertyChoice", "ReadingPropertyChoice",
           "PossiblePropertyChoice")


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
        new_items = self._proxy_items = dict((item.value, item) for item in items)
        self._values = tuple(new_items.keys())
        self._items = tuple(new_items.values())

    def __str__(self):
        return f"{self._items}"

    def __repr__(self):
        return f"{repr(self._items)}"

    @property
    def label(self):
        return self._label

    @property
    def items(self):
        return self._items

    @property
    def values(self):
        return self._values

    def __len__(self):
        return len(self._items)

    def printable_item(self, item_name):
        item_label = self[item_name]
        return f"{self._label} {item_label}"

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item):
        if isinstance(item, Item):
            return item in self._items
        else:
            return item in self._values

    def __getitem__(self, item):
        return self._proxy_items[item]

    def get(self, item, default=None):
        return self._proxy_items.get(item, default)


class MetaChoice(enum.EnumType):
    @property
    def choices(cls):
        result = list()
        for elem in cls:
            choice = elem.value
            result.append(choice.item)

        return result

    def __getitem__(cls, key):
        attr = super().__getitem__(key)
        return attr.value


class Choice(enum.Enum, metaclass=MetaChoice):
    def __str__(self):
        return f"{self.value}"


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


class CardChoices(models.TextChoices, metaclass=MetaStatusChoice):
    pass


class DetectedPropertyChoice(CardChoices):
    DETECTED = "detected", "обнаружен"
    UNDETECTED = "undetected", "не обнаружен"


class SavingPropertyChoice(CardChoices):
    SAVED = "saved", "сохранился"
    UNSAVED = "unsaved", "не сохранился"


class CoveringPropertyChoice(CardChoices):
    COVERED = "covered", "не вскрывался"
    UNCOVERED = "uncovered", "вскрывался"


class ReadingPropertyChoice(CardChoices):
    READABLE = "readable", "читается"
    UNREADABLE = "unreadable", "не читается"


class PossiblePropertyChoice(CardChoices):
    POSSIBLE = "possible", "возможно"
    CONDITIONALLY_POSSIBLE = "conditionally_possible", "условно возможно"
    IMPOSSIBLE = "impossible", "невозможно"
