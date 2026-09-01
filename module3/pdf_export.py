from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

from schemas import StructuredAnswer

# fpdf2's core "Helvetica" font only supports WinAnsi/CP1252, which excludes
# a lot of characters LLMs routinely produce (°, π, ×, ≤, →, bullets, etc.),
# and raises FPDFUnicodeEncodingException the moment one shows up - this bit
# a real user on the deployed app. DejaVu Sans has broad Unicode coverage
# and is bundled here (sourced from matplotlib's redistribution of it,
# Bitstream Vera-derived license - see fonts/LICENSE_DEJAVU) so this works
# the same on Streamlit Cloud's Linux runtime as it does locally.
_FONTS_DIR = Path(__file__).parent / "fonts"
_FONT_FAMILY = "DejaVuSans"


def _register_fonts(pdf: FPDF) -> None:
    pdf.add_font(_FONT_FAMILY, "", str(_FONTS_DIR / "DejaVuSans.ttf"))
    pdf.add_font(_FONT_FAMILY, "B", str(_FONTS_DIR / "DejaVuSans-Bold.ttf"))


def _write(pdf: FPDF, height: int, text: str) -> None:
    """multi_cell that resets the cursor to the left margin afterwards.

    fpdf2's multi_cell defaults to leaving the cursor at the right edge of
    the text it just wrote, so a second call immediately after can be left
    with ~0 width and raise FPDFException("Not enough horizontal space").
    Explicitly returning to the left margin on the next line avoids that.
    """
    pdf.multi_cell(0, height, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def build_pdf(question: str, answer: StructuredAnswer) -> bytes:
    """Render a question + structured answer as a simple one-page PDF."""
    pdf = FPDF()
    _register_fonts(pdf)
    pdf.add_page()

    pdf.set_font(_FONT_FAMILY, "B", 16)
    _write(pdf, 10, "AI Academic Assistant")
    pdf.ln(2)

    _section(pdf, "Question", question)
    _section(pdf, "Explanation", answer.explanation or "-")

    if answer.example:
        _section(pdf, "Example", answer.example)

    if answer.key_insights:
        pdf.set_font(_FONT_FAMILY, "B", 12)
        _write(pdf, 8, "Key Insights")
        pdf.set_font(_FONT_FAMILY, "", 11)
        for insight in answer.key_insights:
            _write(pdf, 7, f"- {insight}")
        pdf.ln(3)

    return bytes(pdf.output())


def _section(pdf: FPDF, heading: str, body: str) -> None:
    pdf.set_font(_FONT_FAMILY, "B", 12)
    _write(pdf, 8, heading)
    pdf.set_font(_FONT_FAMILY, "", 11)
    _write(pdf, 7, body)
    pdf.ln(3)
