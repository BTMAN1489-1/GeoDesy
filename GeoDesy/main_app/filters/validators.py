import uuid
from ..exceptions import BadEnterException


def clean_uuid(data):
    try:
        uuid.UUID(data)
    except Exception:
        raise BadEnterException('UUID указан некорректно.')


def clean_boolean(data):
    if data not in ('1', '0'):
        raise BadEnterException('Boolean указан некорректно.')

