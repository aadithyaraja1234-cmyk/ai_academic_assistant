from pdf_export import build_pdf
from schemas import StructuredAnswer


def test_build_pdf_with_full_answer_produces_valid_pdf_bytes():
    answer = StructuredAnswer(
        explanation="Gravity pulls masses together.",
        example="An apple falls from a tree.",
        key_insights=["Force scales with mass", "Weaker over distance"],
    )

    pdf_bytes = build_pdf("What is gravity?", answer)

    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 0


def test_build_pdf_with_unstructured_fallback_answer_does_not_crash():
    # Regression test: chained multi_cell() calls used to leave the fpdf2
    # cursor at zero available width and raise FPDFException on the
    # second section - see module3/pdf_export.py::_write.
    answer = StructuredAnswer(
        explanation="Some raw, unstructured model output.",
        example="",
        key_insights=[],
        is_structured=False,
    )

    pdf_bytes = build_pdf("What is gravity?", answer)

    assert pdf_bytes.startswith(b"%PDF")
