from datetime import datetime, timedelta
from django.db.models import QuerySet, Q
from django.db import transaction
from django.contrib.auth.base_user import BaseUserManager
import uuid
import config
from main_app import models
from utils import auth_tools
from utils import geo, data, card_tools


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("second_name", "I")
        extra_fields.setdefault("first_name", "am")
        extra_fields.setdefault("third_name", "Boss")
        extra_fields.setdefault("sex", self.model.Sex.UNKNOWN)

        return self.create_user(email, password, **extra_fields)


class SessionQuerySet(QuerySet):
    def create(self, user, **kwargs):
        session = self.model(user=user, api_id=uuid.uuid4(), **kwargs)
        session.save()
        return session


class TFAQuerySet(QuerySet):
    def create(self, **kwargs):
        confirm_code = auth_tools.create_confirm_code()
        tfa_id = uuid.uuid4()
        expired_datetime_code = datetime.utcnow() + timedelta(seconds=config.INTERVAL_CONFIRM_CODE_IN_SECONDS)
        tfa = self.model(tfa_id=tfa_id, confirm_code=confirm_code, expired_datetime_code=expired_datetime_code)
        tfa.save()
        return tfa


class MapQuerySet(QuerySet):
    def nearby_points(self, latitude: float, longitude: float, precision: float):
        pattern_sql = """
with select_by_latitudes as
(
    select * from public.main_app_geopoint
    where abs({latitude:.10g} - latitude)<={precision:.30e}
),
select_by_longitudes as
(
    select * from select_by_latitudes
    where (case 
        when abs(latitude) < 90 then abs({longitude:.10g} - longitude) <= {precision:.30e} / cosd(latitude)
            else true
        end
        )
)

select * from select_by_longitudes;
"""
        raw_sql = pattern_sql.format(latitude=latitude, longitude=longitude, precision=precision)
        return self.raw(raw_sql)

    def _get_min_point_by_distance(self, latitude, longitude, subject_id):
        coord = geo.Coord(latitude=latitude, longitude=longitude)
        radius = config.MIN_DISTANCE_BETWEEN_POINTS
        precision = geo.Geometry.get_precision_by_length(length=radius)
        points = self.nearby_points(coord.degrees.latitude, coord.degrees.longitude, precision)
        if len(points) > 0:
            center_point = geo.Point(coord)
            min_distance = float("inf")
            min_point_by_distance = points[0]

            iter_coord = geo.Coord(0, 0)
            iter_point = geo.Point(iter_coord)

            for p in points:
                iter_coord.update(p.latitude, p.longitude)
                iter_point.update(iter_coord)
                distance = round(geo.Geometry.arc_length(center_point, iter_point), 2)
                if distance < min_distance:
                    min_distance = distance
                    min_point_by_distance = p
                elif distance == min_distance:
                    if p.pk == subject_id:
                        min_point_by_distance = p

            return min_point_by_distance

        return None

    def create(self, latitude: float, longitude: float, subject_code):
        point = self._get_min_point_by_distance(latitude, longitude, subject_code)
        if point is None:
            point = self.model(guid=uuid.uuid4(), latitude=round(latitude, 10), longitude=round(longitude, 10),
                               subject_id=subject_code)

            point.save()
        return point


class CardQueryset(QuerySet):
    def create(self, executor, /, federal_subject, latitude, longitude, photos, **kwargs):
        with transaction.atomic():
            federal_subject_id = data.FEDERAL_SUBJECTS_DICT[federal_subject]
            point = models.GeoPoint.objects.create(latitude, longitude, federal_subject_id)
            card = self.model(card_uuid=uuid.uuid4(), executor=executor, coordinates=point, **kwargs)
            card.save()
            for photo in photos:
                models.Photo(path=photo, card_ref=card).save()

            return card

    def update(self, instance, user, /, **kwargs):
        property_fields = (
            "identification_pillar", "monolith_one", "monolith_two", "monolith_three_and_four", "type_of_sign",
            "sign_height_above_ground_level", "outdoor_sign", "ORP_one", "ORP_two", "trench", "satellite_surveillance"
        )
        with transaction.atomic():
            instance.inspector = user

            for key, value in kwargs.items():
                if key in property_fields:
                    instance.__dict__[key].update(value)

                else:
                    instance.__dict__[key] = value

            instance.datetime_inspection = datetime.utcnow()
            instance.save()

            return instance

    def _create_query_select_cards(self, user, /, only_owned, cards, geopoints, sorted_by, status=None):
        is_staff = user.is_staff
        only_owned_as_inspector = only_owned["as_inspector"]
        only_owned_as_executor = only_owned["as_executor"]
        filter_ = Q()
        if only_owned_as_executor or is_staff:
            if status is not None:
                filter_ &= Q(status=status)

            sub_filter = Q()
            if is_staff and only_owned_as_inspector:
                sub_filter = Q(inspector=user)
            if only_owned_as_executor:
                sub_filter |= Q(executor=user)

            filter_ &= sub_filter

        if cards:
            filter_ &= Q(card_uuid__in=cards)

        if geopoints:
            filter_ &= Q(coordinates__guid__in=geopoints)

        sorted_fields = []
        for item in sorted_by:
            reverse = item["reverse"]
            field_name = "".join(("-", item["field_name"])) if reverse else item["field_name"]
            sorted_fields.append(field_name)

        query = self.filter(filter_).order_by(*sorted_fields).all()

        return query

    def card_info(self, user, /, only_owned, cards, geopoints, sorted_by, limit, offset, displayed_fields=None,
                  status=None):

        query = self._create_query_select_cards(user, only_owned=only_owned, cards=cards,
                                                geopoints=geopoints, sorted_by=sorted_by,
                                                status=status)
        count_rows = query.count()
        query_set = query[offset:(offset + limit)]
        result_list = []
        result = {"cards": result_list, "count": count_rows}

        card_to_dict = card_tools.card_to_dict

        for card in query_set:
            result_list.append(card_to_dict(user, card, displayed_fields))

        return result
