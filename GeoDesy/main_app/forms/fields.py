from django import forms
from ajax_select.fields import AutoCompleteSelectField

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


class FederalSubjectField(AutoCompleteSelectField):
    def get_bound_field(self, form, field_name):
        self.initial = form.instance.coordinates.subject.pk
        return super().get_bound_field(form, field_name)



