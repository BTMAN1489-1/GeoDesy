from datetime import datetime

from rest_framework import serializers
from rest_framework.fields import empty
import ujson
from main_app.exceptions import ValidateError
from main_app.exceptions import NotFoundAPIError
from utils import context, card_tools
from main_app.models import Card

__all__ = (
    "CreateCardForUserSerializer", "UpdateCardForStuffSerializer", "ShowCardSerializer"
)


class BaseCardSerializer(serializers.Serializer):
    def get_value(self, dictionary):
        primitive_value = dictionary.get(self.field_name, None)
        if primitive_value is None:
            return empty
        try:
            dict_data = ujson.decode(primitive_value)

        except ujson.JSONDecodeError:
            return empty
        else:
            return dict_data


class CommentSerializer(serializers.Serializer):
    comment = serializers.CharField(required=False, default=None)


class RecommendationSerializer(serializers.Serializer):
    recommendation = serializers.CharField(required=False, default=None)

    def validate_recommendation(self, value):
        if value is None:
            raise ValidateError(self.error_messages["required"])
        return value


class PropertySerializer(BaseCardSerializer, RecommendationSerializer, CommentSerializer):
    def validate_recommendation(self, value):
        ctx = context.CurrentContext()
        user = ctx.user
        if not user.is_staff:
            return None
        return value


class TypeSignSerializer(BaseCardSerializer):
    value = serializers.ChoiceField(choices=card_tools.TypeSignChoice.choices)
    properties = serializers.DictField(child=serializers.CharField(max_length=255), required=False, default=dict)

    def validate(self, attrs):
        choice_name = attrs["value"]
        choice = card_tools.TypeSignChoice[choice_name]
        sub_choices = choice.sub_items
        raw_data = attrs.pop("properties")
        properties = {}
        for key, value in sub_choices.items():
            property_ = raw_data.get(key, None)
            if property_ is None:
                raise ValidateError(f"Cвойство {choice_name}.{key} обязательно")

            if property_ not in value:
                raise ValidateError(
                    f"Cвойство {choice_name}.{key} не принимает значение '{property_}'."
                    f"Доступные значения: {repr(value)}")
            properties.update({key: property_})

        attrs.update({"properties": properties})

        return attrs


class DetectedProperty(PropertySerializer):
    value = serializers.ChoiceField(choices=card_tools.DetectedPropertyChoice.choices)


class SavingProperty(PropertySerializer):
    value = serializers.ChoiceField(choices=card_tools.SavingPropertyChoice.choices)


class CoveringProperty(PropertySerializer):
    value = serializers.ChoiceField(choices=card_tools.CoveringPropertyChoice.choices)


class ReadingProperty(PropertySerializer):
    value = serializers.ChoiceField(choices=card_tools.ReadingPropertyChoice.choices)


class PossibleProperty(PropertySerializer):
    value = serializers.ChoiceField(choices=card_tools.PossiblePropertyChoice.choices)


class UserInput(serializers.Serializer):
    execute_date = serializers.DateField()
    federal_subject = serializers.ChoiceField(choices=card_tools.FEDERAL_SUBJECTS_NAMES)
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)
    sign_height_above_ground_level = serializers.FloatField()
    sign_height = serializers.FloatField(min_value=0)

    def validate_sign_height_above_ground_level(self, value: float):
        return round(value, 2)

    def validate_sign_height(self, value: float):
        return round(value, 2)


class PhotoSerializer(serializers.Serializer):
    photos = serializers.ListField(child=serializers.ImageField(), min_length=2, allow_empty=False)


class StuffInput(serializers.Serializer):
    point_index = serializers.CharField(max_length=255, required=False)
    name_point = serializers.CharField(required=False)
    year_of_laying = serializers.IntegerField(min_value=1, required=False)
    type_of_center = serializers.CharField(max_length=255, required=False)
    height_above_sea_level = serializers.FloatField(required=False)
    trapezoids = serializers.CharField(required=False)


class CardPropertiesSerializer(serializers.Serializer):
    identification_pillar = DetectedProperty()
    type_of_sign = TypeSignSerializer()
    monolith_one = SavingProperty()
    monolith_two = CoveringProperty()
    monolith_three_and_four = CoveringProperty()
    outdoor_sign = SavingProperty()
    ORP_one = SavingProperty()
    ORP_two = SavingProperty()
    trench = ReadingProperty()
    satellite_surveillance = PossibleProperty()


class CreateCardForUserSerializer(UserInput, PhotoSerializer, CardPropertiesSerializer):

    def create(self, validated_data):
        ctx = context.CurrentContext()
        user = ctx.user
        card = Card.objects.create(user, inspector=None, status=Card.StatusChoice.SENDING, **validated_data)
        return card


class CreateCardForStuffSerializer(UserInput, StuffInput, PhotoSerializer, CardPropertiesSerializer):
    status = serializers.ChoiceField(choices=Card.StatusChoice.choices, default=Card.StatusChoice.SENDING,
                                     required=False)

    def create(self, validated_data):
        ctx = context.CurrentContext()
        user = ctx.user
        card = Card.objects.create(user, inspector=user, datetime_inspection=datetime.utcnow(), **validated_data)
        return card


class UpdateCardForStuffSerializer(StuffInput):
    status = serializers.ChoiceField(choices=Card.StatusChoiceWithOutSending.choices)
    card_uuid = serializers.UUIDField()
    identification_pillar = RecommendationSerializer(required=False)
    type_of_sign = RecommendationSerializer(required=False)
    monolith_one = RecommendationSerializer(required=False)
    monolith_two = RecommendationSerializer(required=False)
    monolith_three_and_four = RecommendationSerializer(required=False)
    outdoor_sign = RecommendationSerializer(required=False)
    ORP_one = RecommendationSerializer(required=False)
    ORP_two = RecommendationSerializer(required=False)
    trench = RecommendationSerializer(required=False)
    satellite_surveillance = RecommendationSerializer(required=False)

    def create(self, validated_data):
        copy_data = validated_data.copy()
        card_uuid = copy_data.pop("card_uuid")
        try:

            card = Card.objects.get(card_uuid=card_uuid)

        except Card.DoesNotExist:
            raise NotFoundAPIError(f'Объект с card_id({card_uuid}) не существует.')

        ctx = context.CurrentContext()
        user = ctx.user
        update_card = Card.objects.update(card, user, **copy_data)
        return update_card


class SortedField(serializers.Serializer):
    field_name = serializers.ChoiceField(choices=card_tools.sorted_fields)
    reverse = serializers.BooleanField(required=False, default=False)


class OwnedCardField(serializers.Serializer):
    as_executor = serializers.BooleanField()
    as_inspector = serializers.BooleanField(required=False, default=False)


class ShowCardSerializer(serializers.Serializer):
    cards = serializers.ListField(child=serializers.UUIDField(), required=False, max_length=100, default=list)
    geopoints = serializers.ListField(child=serializers.UUIDField(), required=False, max_length=100, default=list)
    displayed_fields = serializers.ListField(child=serializers.ChoiceField(choices=card_tools.displayed_fields),
                                             required=False, allow_empty=True, max_length=100)

    sorted_by = serializers.ListField(child=SortedField(), required=False, allow_null=True, default=list)
    status = serializers.ChoiceField(choices=Card.StatusChoice, required=False, allow_null=True, default=None)
    limit = serializers.IntegerField(min_value=0, max_value=1000, required=False, default=100)
    offset = serializers.IntegerField(min_value=0, max_value=1000, required=False, default=0)
    only_owned = OwnedCardField(required=False, default={"as_executor": True, "as_inspector": False})

    def create(self, validated_data):
        ctx = context.CurrentContext()
        user = ctx.user

        ctx.response = Card.objects.card_info(user, **validated_data)
        return user
