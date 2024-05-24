from ..exceptions import BadEnterException


class FilterField:
    def __init__(self, search_name, filter_name, validators=(), required=False):
        self._validators = validators
        self._search_name = search_name
        self._filter_name = filter_name
        self._required = required

    @property
    def validators(self):
        return self._validators

    @property
    def search_name(self):
        return self._search_name

    @property
    def filter_name(self):
        return self._filter_name

    def clean(self, data):
        if data is None:
            if self._required:
                raise BadEnterException(f"Параметр {self._search_name} обязателен.")
            return

        for validator in self._validators:
            validator(data)


class BaseFilter:
    _prefix = "field"

    @classmethod
    def filter(cls, data: dict):
        filter_dict = {}
        for field in cls.get_fields():
            value = data.get(field.search_name, None)
            field.clean(value)
            if value is not None:
                filter_dict.update({field.filter_name: value})

        return filter_dict

    @classmethod
    def get_fields(cls):
        fields = []
        for key in cls.__dict__:
            if key.startswith(cls._prefix):
                fields.append(cls.__dict__[key])

        return fields
