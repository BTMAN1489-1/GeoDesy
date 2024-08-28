from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils import formats
from datetime import datetime
from main_app.forms import CardForm
from main_app.models import Card
from utils.card_tools import printable_type_of_sign
from dalf.admin import DALFModelAdmin, DALFRelatedOnlyField


def _create_user_info_context(user, datetime_field):
    context = user.get_user_info
    context["datetime"] = {"label": datetime_field.verbose_name, "value": formats.localize(datetime_field)}
    return context


@admin.register(Card)
class CardAdmin(DALFModelAdmin):
    form = CardForm
    readonly_fields = ("photos", "execution", "inspection", "geo_info", "type_of_sign_desc")
    fields = (
        "photos", "subject", "geo_info", "execution", "inspection", "sign_height_above_ground_level",
        "type_of_sign_desc", "identification_pillar", "monolith_one", "monolith_two", "monolith_three_and_four",
        "outdoor_sign", "ORP_one", "ORP_two", "trench", "satellite_surveillance", "point_index", "name_point",
        "year_of_laying", "type_of_center", "height_above_sea_level", "trapezoids", "status",
    )
    list_display = ("card_uuid", "coordinates", "federal_subject", "datetime_creation", "datetime_inspection", "status")
    # search_fields = ("coordinates",)
    list_per_page = 10
    list_filter = (
        ("coordinates__subject", DALFRelatedOnlyField),
        ("coordinates__subject__district", DALFRelatedOnlyField),
        "status"
    )

    def response_change(self, request, obj):
        if "_download_pdf" in request.POST:
            return redirect("download_card", obj.card_uuid)
        return super().response_change(request, obj)

    @admin.display(description="Субъект РФ")
    def federal_subject(self, obj):
        return obj.coordinates.federal_subject

    @admin.display(description="Фотографии")
    def photos(self, obj):
        return render_to_string("admin/main_app/photo/photos.html", {"photos": obj.photos.all()})

    @admin.display(description="Тип знака")
    def type_of_sign_desc(self, obj):
        type_of_sign = obj.type_of_sign
        context = {"properties": printable_type_of_sign(type_of_sign)}
        return render_to_string("admin/main_app/card/type_of_sign.html", context)

    @admin.display(description="Информация о создании")
    def execution(self, obj):
        context = {"card": obj, "user": obj.executor, "label_fio": "ФИО исполнителя",
                   "label_email": "E-mail исполнителя"}
        return render_to_string("admin/main_app/card/execution_desc.html", context)

    @admin.display(description="Информация о проверке")
    def inspection(self, obj):
        context = {"card": obj, "user": obj.inspector, "label_fio": "ФИО проверяющего",
                   "label_email": "E-mail проверяющего"}
        return render_to_string("admin/main_app/card/inspection_desc.html", context)

    @admin.display(description="Местоположение")
    def geo_info(self, obj):
        context = {"geo": obj.coordinates}
        return render_to_string("admin/main_app/geo/base_geo.html", context)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.inspector = request.user
        obj.datetime_inspection = datetime.utcnow()
        subject = form.cleaned_data['subject']
        obj.coordinates.subject = subject
        obj.coordinates.save()
        obj.save()

    def has_download_pdf_card(self, obj):
        if obj.status == Card.SuccessChoice.SUCCESS:
            return True
        else:
            return False

    def render_change_form(
            self, request, context, add=False, change=False, form_url="", obj=None
    ):
        context.update({"show_open_pdf_button": self.has_download_pdf_card(obj)})
        return super().render_change_form(request, context, add, change, form_url, obj)
