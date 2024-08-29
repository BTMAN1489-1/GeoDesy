from abc import ABC, abstractmethod
from contextvars import ContextVar
from typing import Iterable

from fpdf import FontFace
from fpdf.enums import TableSpan
from main_app.models import Card
from utils.pdf.helpers import *
from django.utils.formats import localize
from utils.card_tools import printable_coordinates, printable_type_of_sign, printable_sign_height_above_ground_level

__all__ = (
    "BaseNode", "ExecuteDateNode", "InstitutionNode", "FederalSubjectNode", "ExecutorInfoNode", "CoordinatesNode",
    "PointIndexInfoNode", "PointNameInfoNode", "YearOfLayingNode", "SignHeightNode", "TypeOfCenterNode",
    "HeightAboveSeaLevelNode", "TrapezoidsNode", "TypeOfSignNode", "SignHeightAboveGroundLevelNode",
    "CardPropertyTableTemplate", "PhotosNode", "_representation_nodes", "ctx_card_data", "HeadingCellTemplate",
    "ValueCellTemplate", "ExecutorSignatureTableTemplate", "InspectorSignatureTableTemplate", "BaseTableTemplate"
)

ctx_card_data = ContextVar("card_data")

HeadingCellTemplate = CardCell(
    style=FontFace("DejaVu", emphasis="B", size_pt=12, fill_color=(137, 173, 191)),
    align="L",
    padding=(0, 5, 0, 5)
)

ValueCellTemplate = CardCell(
    style=FontFace("DejaVu", emphasis="I", size_pt=11, fill_color=(225, 236, 236)),
    align="C"
)


def _non_empty_localize(value, pattern: str, use_l10n=None, empty_string="-"):
    repr_value = localize(value, use_l10n)
    if repr_value:
        return pattern % repr_value
    else:
        return empty_string


class BaseNode(ABC):

    @abstractmethod
    def to_representation(self):
        raise NotImplementedError()


class ExecuteDateNode(BaseNode):

    def to_representation(self):
        card_data = ctx_card_data.get()
        header = HeadingCellTemplate.replace(text="Дата проведения работ")
        value = ValueCellTemplate.replace(text=_non_empty_localize(card_data.card.execute_date, "%s"))
        return header, value


class InstitutionNode(BaseNode):

    def to_representation(self):
        return (ValueCellTemplate.replace(text="Управление Росреестра по Приморскому краю"),)


class FederalSubjectNode(BaseNode):

    def to_representation(self):
        card_data = ctx_card_data.get()
        header = HeadingCellTemplate.replace(text="Субъект РФ")
        value = ValueCellTemplate.replace(text=_non_empty_localize(card_data.coordinates.federal_subject, "%s"))
        return header, value


class ExecutorInfoNode(BaseNode):

    def to_representation(self):
        card_data = ctx_card_data.get()
        header = HeadingCellTemplate.replace(text="Кем выполнены работы")
        value = ValueCellTemplate.replace(text=card_data.executor.full_name)
        return header, value


class CoordinatesNode(BaseNode):

    def to_representation(self):
        card_data = ctx_card_data.get()
        header = HeadingCellTemplate.replace(text="Координаты пункта")
        value = ValueCellTemplate.replace(text="      ".join(printable_coordinates(card_data.coordinates)))
        return header, value


class PointIndexInfoNode(BaseNode):

    def to_representation(self):
        card_data = ctx_card_data.get()
        header = HeadingCellTemplate.replace(text="№ по каталогу/индекс пункта")
        value_text = _non_empty_localize(card_data.card.point_index, "%s")
        value = ValueCellTemplate.replace(text=value_text)
        return header, value


class PointNameInfoNode(BaseNode):

    def to_representation(self):
        card_data = ctx_card_data.get()
        header = HeadingCellTemplate.replace(text="Название пункта, класс, № марки")
        value_text = _non_empty_localize(card_data.card.name_point, "%s")
        value = ValueCellTemplate.replace(text=value_text)
        return header, value


class YearOfLayingNode(BaseNode):

    def to_representation(self):
        card_data = ctx_card_data.get()
        header = HeadingCellTemplate.replace(text="Год закладки")
        value_text = _non_empty_localize(card_data.card.year_of_laying, "%sг")
        value = ValueCellTemplate.replace(text=value_text)
        return header, value


class SignHeightNode(BaseNode):

    def to_representation(self):
        card_data = ctx_card_data.get()
        header = HeadingCellTemplate.replace(text="Высота знака")
        value = ValueCellTemplate.replace(text=f"{localize(card_data.card.sign_height)}м")
        return header, value


class TypeOfCenterNode(BaseNode):

    def to_representation(self):
        card_data = ctx_card_data.get()
        header = HeadingCellTemplate.replace(text="Тип центра")
        value_text = _non_empty_localize(card_data.card.type_of_center, "%s")
        value = ValueCellTemplate.replace(text=value_text)
        return header, value


class HeightAboveSeaLevelNode(BaseNode):
    def to_representation(self):
        card_data = ctx_card_data.get()
        header = HeadingCellTemplate.replace(text="Высота над уровнем моря")
        value_text = _non_empty_localize(card_data.card.height_above_sea_level, "%sм")
        value = ValueCellTemplate.replace(text=value_text)
        return header, value


class TrapezoidsNode(BaseNode):
    def to_representation(self):
        card_data = ctx_card_data.get()
        header = HeadingCellTemplate.replace(text="Трапеции")
        value_text = _non_empty_localize(card_data.card.trapezoids, "%s")
        value = ValueCellTemplate.replace(text=value_text)
        return header, value


class TypeOfSignNode(BaseNode):
    def to_representation(self):
        card_data = ctx_card_data.get()
        header = HeadingCellTemplate.replace(text="Тип знака")
        values = (ValueCellTemplate.replace(text=value) for value in
                  printable_type_of_sign(card_data.card.type_of_sign))
        return header, *values


class SignHeightAboveGroundLevelNode(BaseNode):

    def to_representation(self):
        card_data = ctx_card_data.get()
        header = HeadingCellTemplate.replace(text="Высота верхней марки")
        height = card_data.card.sign_height_above_ground_level
        value = ValueCellTemplate.replace(text=printable_sign_height_above_ground_level(height))
        return header, value


class PhotosNode(BaseNode):

    def to_representation(self):
        card_data = ctx_card_data.get()
        photos = map(lambda photo: CardCell(img=photo.absolute_path), card_data.photos)
        header = HeadingCellTemplate.replace(text="Фотографии пункта", align="C")
        values = CardCellCollection(cells=photos, default_style_cell=CardCell(img_fill_width=True))

        return header, *values


def _representation_nodes(nodes: Iterable[BaseNode]):
    return map(lambda node: node.to_representation(), nodes)


class BaseTableTemplate(ABC):
    @abstractmethod
    def render(self):
        raise NotImplementedError()


class CardPropertyTableTemplate(BaseTableTemplate):
    def __init__(self, property_class, property_name):
        if hasattr(Card, property_name):
            self._property_class = property_class
            self._property_name = property_name
            card_prop = getattr(Card, property_name)
            self._property_label = card_prop.field.verbose_name
        else:
            raise AttributeError(f"There is no {property_name} field in the model card")

    def render(self):
        card = ctx_card_data.get().card
        property_name = self._property_name
        property_value = getattr(card, property_name)
        choice = self._property_class[property_value["value"].upper()]
        headers = CardCellCollection(cells=(
            CardCell(text=self._property_label),
            CardCell(text="Состояние"),
            CardCell(text="Рекомендация"),

        ), default_style_cell=HeadingCellTemplate)
        values = CardCellCollection(cells=(
            CardCell(text=choice.label),
            CardCell(text=_non_empty_localize(property_value["recommendation"], "%s")),

        ), default_style_cell=ValueCellTemplate)
        return (*headers,), (TableSpan.COL, *values,)


class ExecutorSignatureTableTemplate(BaseTableTemplate):
    def render(self):
        card_data = ctx_card_data.get()
        exec_header = CardCell(text="Составил",
                               style=FontFace("DejaVu", emphasis="B", size_pt=11),
                               align="L")

        return (
            (exec_header, CardCell(
                text=localize(card_data.card.datetime_creation.date()),
                style=FontFace("DejaVu", emphasis="I", size_pt=10),
                align="L",
                padding=(0, 5, 0, 5)
            )),
            (TableSpan.COL, CardCell(
                text=card_data.executor.full_name,
                style=FontFace("DejaVu", emphasis="I", size_pt=10),
                align="L",
                padding=(0, 5, 0, 5)
            )),
        )


class InspectorSignatureTableTemplate(BaseTableTemplate):
    def render(self):
        card_data = ctx_card_data.get()

        inspect_header = CardCell(text="Проверил",
                                  style=FontFace("DejaVu", emphasis="B", size_pt=11),
                                  align="L")

        return (
            (inspect_header,
             CardCell(
                 text=localize(card_data.card.datetime_inspection.date()),
                 style=FontFace("DejaVu", emphasis="I", size_pt=10),
                 align="L",
                 padding=(0, 5, 0, 5))),
            (TableSpan.COL, CardCell(
                text=card_data.inspector.full_name,
                style=FontFace("DejaVu", emphasis="I", size_pt=10),
                align="L",
                padding=(0, 5, 0, 5)
            )),
        )
