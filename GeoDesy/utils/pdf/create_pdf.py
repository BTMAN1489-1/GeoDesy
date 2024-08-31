from typing import Iterable
from fpdf import FPDF
from fpdf.enums import TableSpan, TableHeadingsDisplay
from itertools import zip_longest, islice
from more_itertools import batched
from utils.pdf.helpers import *
from utils.pdf.representation import *
from utils.card_tools.data import CardData
from utils.card_tools.choices import *
from contextvars import copy_context
from geodesy import settings

__all__ = (
    "DynamicRowTable", "CardPDF"
)

DefaultTableParameters = TableParameters(
    align="C", first_row_as_headings=False, v_align="M", gutter_width=1, gutter_height=1,
)

HEADER_CONTENT: Iterable[BaseNode] = (ExecuteDateNode(), InstitutionNode(), FederalSubjectNode(), ExecutorInfoNode(),
                                      CoordinatesNode())

MAIN_CONTENT: Iterable[BaseNode] = (PointIndexInfoNode(), PointNameInfoNode(), YearOfLayingNode(), SignHeightNode(),
                                    TypeOfCenterNode(), HeightAboveSeaLevelNode(), TrapezoidsNode(),
                                    TypeOfSignNode(), SignHeightAboveGroundLevelNode())

PHOTO_CONTENT: Iterable[BaseNode] = (PhotosNode(),)

IdentificationPillarProperty = CardPropertyTableTemplate(DetectedPropertyChoice, "identification_pillar")
MonolithOneProperty = CardPropertyTableTemplate(SavingPropertyChoice, "monolith_one")
MonolithTwoProperty = CardPropertyTableTemplate(CoveringPropertyChoice, "monolith_two")
MonolithThreeAndFourProperty = CardPropertyTableTemplate(CoveringPropertyChoice, "monolith_three_and_four")
OutdoorSignProperty = CardPropertyTableTemplate(SavingPropertyChoice, "outdoor_sign")
ORPOneProperty = CardPropertyTableTemplate(SavingPropertyChoice, "ORP_one")
ORPTwoProperty = CardPropertyTableTemplate(SavingPropertyChoice, "ORP_two")
TrenchProperty = CardPropertyTableTemplate(ReadingPropertyChoice, "trench")
SatelliteSurveillanceProperty = CardPropertyTableTemplate(PossiblePropertyChoice, "satellite_surveillance")

CARD_PROPERTIES_CONTENT: Iterable[BaseTableTemplate] = (
    IdentificationPillarProperty, MonolithOneProperty, MonolithTwoProperty,
    MonolithThreeAndFourProperty, OutdoorSignProperty, ORPOneProperty,
    ORPTwoProperty,
    TrenchProperty, SatelliteSurveillanceProperty
)

INSPECTOR_SIGNATURE: BaseTableTemplate = InspectorSignatureTableTemplate()
EXECUTOR_SIGNATURE: BaseTableTemplate = ExecutorSignatureTableTemplate()


class DynamicRowTable:

    def __new__(cls, content_list: Iterable[CardCell | TableSpan], cols: int):
        result = []
        for batch in batched(content_list, cols):
            length_row = len(batch)
            table = list(zip_longest(*(islice(seq, 0, None) for seq in batch), fillvalue=TableSpan.ROW))
            if length_row < cols:
                count_empty_cols = cols - length_row
                for i in range(len(table)):
                    value = table[i][-1]
                    match value:
                        case TableSpan.ROW:
                            table[i] += (TableSpan.ROW,) * count_empty_cols
                        case _:
                            table[i] += (TableSpan.COL,) * count_empty_cols

            result.extend(table)
        return result


class CardPDF(FPDF):
    author = "GeoDesy corp."
    main_title = "Карточка исследования пункта ГГС"

    def __init__(self, obj_model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_fonts()
        self.setup_document()
        ctx = copy_context()
        ctx.run(self._create, CardData(obj_model))

    def setup_fonts(self):
        self.add_font('DejaVu', '', settings.BASE_DIR / 'static/fonts/DejaVuSansCondensed.ttf')
        self.add_font('DejaVu', 'B', settings.BASE_DIR / 'static/fonts/DejaVuSansCondensed-Bold.ttf')
        self.add_font('DejaVu', 'I', settings.BASE_DIR / 'static/fonts/DejaVuSansCondensed-Oblique.ttf')
        self.add_font('DejaVu', 'BI', settings.BASE_DIR / 'static/fonts/DejaVuSansCondensed-BoldOblique.ttf')

    def setup_document(self):
        self.set_author(self.author)
        self.set_margin(15)

    def header(self):
        self.set_font("DejaVu", "B", 15)

        self.cell(text=self.main_title, align="L")
        self.cell(w=self.w - self.x - self.r_margin, text=self.author, align="R")
        self.ln(8)
        self.line(self.l_margin, self.y, self.w - self.r_margin, self.y)

        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 10)
        self.line(self.l_margin, self.y, self.w - self.r_margin, self.y)
        self.cell(0, 10, f"{self.page_no()}/{{nb}}", align="C")

    def print_table(self, table_schema, count_cols, table_parameters: TableParameters):
        table_data = DynamicRowTable(table_schema, count_cols)
        with self.table(table_data, **table_parameters):
            pass

    def _create(self, card_data):
        ctx_card_data.set(card_data)

        self.add_page()
        table_params = DefaultTableParameters
        repr_content = _representation_nodes

        self.print_table(repr_content(HEADER_CONTENT), 2, table_params)
        self.ln(5)

        self.print_table(repr_content(MAIN_CONTENT), 2, table_params)

        self.add_page()

        props = CARD_PROPERTIES_CONTENT
        for prop in props:
            self.print_table(prop.render(), 4, table_params.replace(
                repeat_headings=TableHeadingsDisplay.ON_TOP_OF_EVERY_PAGE, first_row_as_headings=True))
            self.ln(6)

        self.add_page()
        self.print_table(repr_content(PHOTO_CONTENT), 1,
                         table_params.replace(borders_layout="ALL",
                                              repeat_headings=TableHeadingsDisplay.ON_TOP_OF_EVERY_PAGE,
                                              first_row_as_headings=True,
                                              gutter_height=3)
                         )
        self.add_page()
        self.print_table(EXECUTOR_SIGNATURE.render(), 2,
                         table_params.replace(
                             borders_layout="NONE",
                             repeat_headings=TableHeadingsDisplay.ON_TOP_OF_EVERY_PAGE,
                             first_row_as_headings=True,
                             gutter_width=0, gutter_height=0
                         ))
        self.line(self.l_margin, self.y, self.w - self.r_margin, self.y)
        self.ln(5)

        self.print_table(INSPECTOR_SIGNATURE.render(), 2,
                         table_params.replace(
                             borders_layout="NONE",
                             repeat_headings=TableHeadingsDisplay.ON_TOP_OF_EVERY_PAGE,
                             first_row_as_headings=True,
                             gutter_width=0, gutter_height=0
                         ))
        self.line(self.l_margin, self.y, self.w - self.r_margin, self.y)
