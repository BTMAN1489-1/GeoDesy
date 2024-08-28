import datetime
from django import forms
from utils import card_tools
from .widgets import CardPropertyWidget
from .fields import CardPropertyField, FederalSubjectField
from main_app.models import Card


class CardForm(forms.ModelForm):
    status = forms.ChoiceField(widget=forms.RadioSelect, label="Изменить статус заявки", required=True,
                               initial=Card.PendingChoice.PENDING,
                               choices=Card.StatusChoiceWithOutSending.choices)

    identification_pillar = CardPropertyField(
        widget=CardPropertyWidget(class_property=card_tools.DetectedPropertyChoice),
        label="Опознавательный столб", required=False)

    monolith_one = CardPropertyField(widget=CardPropertyWidget(class_property=card_tools.SavingPropertyChoice),
                                     label="Монолит I", required=False)

    monolith_two = CardPropertyField(widget=CardPropertyWidget(class_property=card_tools.CoveringPropertyChoice),
                                     label="Монолит II", required=False)

    monolith_three_and_four = CardPropertyField(
        widget=CardPropertyWidget(class_property=card_tools.CoveringPropertyChoice),
        label="Монолиты III и IV", required=False)

    outdoor_sign = CardPropertyField(widget=CardPropertyWidget(class_property=card_tools.SavingPropertyChoice),
                                     label="Наружный знак", required=False)

    ORP_one = CardPropertyField(widget=CardPropertyWidget(class_property=card_tools.SavingPropertyChoice),
                                label="ОРП I", required=False)

    ORP_two = CardPropertyField(widget=CardPropertyWidget(class_property=card_tools.SavingPropertyChoice),
                                label="ОРП II", required=False)

    trench = CardPropertyField(widget=CardPropertyWidget(class_property=card_tools.ReadingPropertyChoice),
                               label="Окопка", required=False)

    satellite_surveillance = CardPropertyField(
        widget=CardPropertyWidget(class_property=card_tools.PossiblePropertyChoice),
        label="Спутниковое наблюдение на пункте", required=False)

    year_of_laying = forms.IntegerField(min_value=1, max_value=datetime.date.today().year, label="Год закладки",
                                        required=False)
    sign_height_above_ground_level = forms.FloatField(label="Высота верхней марки",
                                                      help_text="Высота может быть и отрицательной. Данный параметр скорее показывает отклонение относительно уровня земли.",
                                                      disabled=True, required=False)

    subject = FederalSubjectField('subjects', label="Субъект РФ", help_text="Начните ввод для поиска",
                                  show_help_text=False)

    def _clean_fields(self):
        for name, bf in self._bound_items():
            field = bf.field
            value = bf.initial if field.disabled else bf.value()
            try:
                if isinstance(field, forms.FileField):
                    value = field.clean(value, bf.initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, "clean_%s" % name):
                    value = getattr(self, "clean_%s" % name)()
                    self.cleaned_data[name] = value
            except forms.ValidationError as e:
                self.add_error(name, e)
