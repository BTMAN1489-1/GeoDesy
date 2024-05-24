from main_app import exceptions

try:
    import ujson as json
except ImportError:
    import json


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance


def serialize_to_json(data: dict):
    try:
        serialized_data = json.dumps(data)
    except Exception as ex:
        raise exceptions.JsonSerializeError(ex)
    else:
        return serialized_data.encode('UTF-8')


def deserialize_to_dict(row_json):
    try:
        serialized_data = json.loads(row_json)
    except Exception as ex:
        raise exceptions.JsonDeserializeError(ex)
    else:
        return serialized_data
