from django.utils.formats import localize
from .data import displayed_fields, displayed_Card_fields, displayed_GeoPoint_fields, owners
from .choices import TypeSignChoice

__all__ = ("card_to_dict", "printable_type_of_sign", "printable_coordinates",
           "printable_sign_height_above_ground_level")


def card_to_dict(user, card, allow_fields):
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


def printable_type_of_sign(type_of_sign: dict) -> list[str]:
    type_of_sign_name = type_of_sign["value"]
    type_of_sign_item = TypeSignChoice[type_of_sign_name]
    desc = [type_of_sign_item.label.capitalize()]
    sub_items = type_of_sign_item.sub_items
    properties = type_of_sign["properties"]
    for key, array_item in sub_items.items():
        sub_item_name = properties[key]
        desc.append(array_item.printable_item(sub_item_name).capitalize())

    return desc


def printable_coordinates(coord):
    latitude = coord.latitude
    longitude = coord.longitude
    latitude_sign = "N" if latitude >= 0 else "S"
    longitude_sign = "E" if longitude >= 0 else "W"
    return [
        "".join((latitude_sign, localize(abs(latitude)), u"\u00b0")),
        "".join((longitude_sign, localize(abs(longitude)), u"\u00b0")),
    ]


def printable_sign_height_above_ground_level(sign_height_above_ground_level: float):
    s = "Выше" if sign_height_above_ground_level >= 0 else "Ниже"
    return f"{s} уровня земли на {localize(abs(sign_height_above_ground_level))}м"
