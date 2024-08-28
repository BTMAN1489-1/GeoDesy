from collections.abc import Mapping, Collection
from dataclasses import dataclass, field, replace
from typing import Optional, Union, Iterable
from fpdf import Align, FontFace
from fpdf.drawing import DeviceGray, DeviceRGB
from fpdf.enums import VAlign, TableCellFillMode, TableBordersLayout, WrapMode, TableHeadingsDisplay
from fpdf.util import Padding

__all__ = ("CardCell", "CardCellCollection", "TableParameters")


class NonEmptyMapping(dict):
    def __iter__(self):
        return (key for key, value in self.items() if value is not None)

    def __getitem__(self, item):
        return getattr(self, item, None)

    def items(self):
        return vars(self).items()

    def keys(self):
        return iter(self)

    def __len__(self):
        return len(vars(self))


@dataclass(frozen=True)
class NonEmptyDataclass(NonEmptyMapping):
    def replace(self, **kwargs):
        return replace(self, **kwargs)


@dataclass(frozen=True)
class CardCell(NonEmptyDataclass):
    text: Optional[str] = field(default=None)
    align: Optional[Union[str, Align]] = field(default=None)
    v_align: Optional[Union[str, VAlign]] = field(default=None)
    style: Optional[FontFace] = field(default=None)
    img: Optional[str] = field(default=None)
    colspan: Optional[int] = field(default=None)
    rowspan: Optional[int] = field(default=None)
    img_fill_width: Optional[bool] = field(default=None)
    padding: Optional[Union[int, tuple, type(None)]] = field(default=None)
    link: Optional[Union[str, int]] = field(default=None)


class CardCellCollection(Collection):
    def __init__(self, cells: Iterable[CardCell], default_style_cell: CardCell):
        self._default_style_cell = default_style_cell
        self._cells = tuple(cells)

    def __contains__(self, item):
        if isinstance(item, CardCell):
            _cells = self._cells
            for cell in _cells:
                if cell == item:
                    return True

            return False

        raise TypeError()

    def __iter__(self):
        style_template = self._default_style_cell
        _cells = self._cells
        return (style_template.replace(**cell) for cell in _cells)

    def __add__(self, other: Iterable[CardCell]) -> list[CardCell]:
        return [*self, *other]

    def __len__(self):
        return len(self._cells)


@dataclass(frozen=True)
class TableParameters(NonEmptyDataclass):
    align: Optional[Union[str, Align]] = field(default=None)
    v_align: Optional[Union[str, VAlign]] = field(default=None)
    borders_layout: Optional[Union[TableBordersLayout, str]] = field(default=None)
    cell_fill_color: Optional[Union[float, tuple, DeviceGray, DeviceRGB]] = field(default=None)
    cell_fill_mode: Optional[Union[str, TableCellFillMode]] = field(default=None)
    col_widths: Optional[Union[float, tuple]] = field(default=None)
    first_row_as_headings: Optional[bool] = field(default=None)
    gutter_height: Optional[float] = field(default=None)
    gutter_width: Optional[float] = field(default=None)
    headings_style: Optional[FontFace] = field(default=None)
    line_height: Optional[float] = field(default=None)
    markdown: Optional[bool] = field(default=None)
    text_align: Optional[Union[str, Align, tuple]] = field(default=None)
    width: Optional[float] = field(default=None)
    wrapmode: Optional[WrapMode] = field(default=None)
    padding: Optional[Union[float, tuple, Padding]] = field(default=None)
    outer_border_width: Optional[float] = field(default=None)
    num_heading_rows: Optional[int] = field(default=None)
    repeat_headings: Optional[TableHeadingsDisplay] = field(default=None)
