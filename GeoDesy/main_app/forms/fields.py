from django import forms
from main_app.exceptions import ValidateError

from utils import card_tools
import copy
from main_app.forms import widgets


class CardPropertyBoundField(forms.BoundField):
    def value(self):
        """
        Return the value for this BoundField, using the initial value if
        the form is not bound or the data otherwise.
        """
        data = self.initial
        if self.form.is_bound:
            data["recommendation"] = self.field.bound_data(self.data, data)
        return self.field.prepare_value(data)


class CardPropertyField(forms.Field):
    def get_bound_field(self, form, field_name):
        return CardPropertyBoundField(form, self, field_name)


class UserInfoField(forms.Field):

    widget = widgets.UserInfoWidget

    def __init__(
            self,
            *,
            label=None,
            help_text="",
            error_messages=None,
            localize=False,
            label_suffix=None,
    ):
        super().__init__(
            required=False,
            label=label,
            initial=None,
            help_text=help_text,
            error_messages=error_messages,
            show_hidden_initial=False,
            validators=(),
            localize=localize,
            disabled=False,
            label_suffix=label_suffix,
            template_name=None,
        )


