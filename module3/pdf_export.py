from fpdf import FPDF
from fpdf.enums import XPos, YPos

from schemas import StructuredAnswer


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
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    _write(pdf, 10, "AI Academic Assistant")
    pdf.ln(2)

    _section(pdf, "Question", question)
    _section(pdf, "Explanation", answer.explanation or "-")

    if answer.example:
        _section(pdf, "Example", answer.example)

    if answer.key_insights:
        pdf.set_font("Helvetica", "B", 12)
        _write(pdf, 8, "Key Insights")
        pdf.set_font("Helvetica", "", 11)
        for insight in answer.key_insights:
            _write(pdf, 7, f"- {insight}")
        pdf.ln(3)

    return bytes(pdf.output())


def _section(pdf: FPDF, heading: str, body: str) -> None:
    pdf.set_font("Helvetica", "B", 12)
    _write(pdf, 8, heading)
    pdf.set_font("Helvetica", "", 11)
    _write(pdf, 7, body)
    pdf.ln(3)
