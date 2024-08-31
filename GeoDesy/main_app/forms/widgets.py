from django import forms

__all__ = (
    "RecommendationWidget", "CardPropertyWidget"
)


class RecommendationWidget(forms.Textarea):
    template_name = "admin/main_app/card/widgets/card_property.html"

    def __init__(self, *args, **kwargs):
        default_attrs = {"cols": "20", "rows": "2"}
        super().__init__(default_attrs)

    def _prepare_value(self, value) -> dict:
        raise NotImplementedError()

    def get_context(self, name, value, attrs):
        new_value = {"description": self._prepare_value(value)}
        comment = value.get("comment", None)
        if comment is not None:
            new_value.update({"comment": {"label": "Комментарий", "value": comment}})

        recommendation = value.get("recommendation", None)
        new_value.update({"recommendation": {"label": "Рекомендация", "value": recommendation}})

        return {
            "widget": {
                "name": name,
                "is_hidden": self.is_hidden,
                "required": self.is_required,
                "value": new_value,
                "attrs": self.build_attrs(self.attrs, attrs),
                "template_name": self.template_name,
            },
        }


class CardPropertyWidget(RecommendationWidget):

    def __init__(self, /, class_property, **kwargs):
        self.class_property = class_property
        super().__init__(**kwargs)

    def _get_property(self, name):
        return self.class_property[name.upper()]

    def _prepare_value(self, value):
        property_name = value.get("value", "")
        property_ = self._get_property(property_name)
        description = [property_.label.capitalize()]

        new_value = {"value": description, "label": "Состояние"}

        return new_value
