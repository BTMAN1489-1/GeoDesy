from django.contrib import admin
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils import formats
from datetime import datetime
import config
from main_app.forms import CardForm
from main_app.models import Card, GeoPoint, User, Photo


def _create_user_info_context(user, datetime_field):
    context = user.get_user_info
    context["datetime"] = {"label": datetime_field.verbose_name, "value": formats.localize(datetime_field)}
    return context


@admin.register(Card)
class MyModelModelAdmin(admin.ModelAdmin):
    form = CardForm
    readonly_fields = ("photos", "execution", "inspection", "geo_info")
    fields = (
        "photos", "geo_info", "execution", "inspection", "sign_height_above_ground_level",
        "type_of_sign", "identification_pillar", "monolith_one", "monolith_two", "monolith_three_and_four",
        "outdoor_sign", "ORP_one", "ORP_two", "trench", "satellite_surveillance", "point_index", "name_point",
        "year_of_laying", "type_of_center", "height_above_sea_level", "trapezoids", "status"
    )
    list_display = ("coordinates",)

    @admin.display(description="Фотографии")
    def photos(self, obj):
        return mark_safe(render_to_string("admin/main_app/photo/photos.html", {"photos": obj.photos.all()}))

    @admin.display(description="Информация о создании")
    def execution(self, obj):
        context = {"card": obj, "user": obj.executor, "label_fio": "ФИО исполнителя",
                   "label_email": "E-mail исполнителя"}
        return mark_safe(render_to_string("admin/main_app/card/execution_desc.html", context))

    @admin.display(description="Информация о проверке")
    def inspection(self, obj):
        context = {"card": obj, "user": obj.inspector, "label_fio": "ФИО проверяющего",
                   "label_email": "E-mail проверяющего"}
        return mark_safe(render_to_string("admin/main_app/card/inspection_desc.html", context))

    @admin.display(description="Местоположение")
    def geo_info(self, obj):
        context = {"map_api_key": config.MAP_API_KEY, "geo": obj.coordinates}
        return mark_safe(render_to_string("admin/main_app/geo/base_geo.html", context))

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.inspector = request.user
        obj.datetime_inspection = datetime.utcnow()
        obj.save()



