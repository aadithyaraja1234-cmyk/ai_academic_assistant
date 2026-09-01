# 🎓 AI Academic Assistant

[![CI](https://github.com/aadithyaraja1234-cmyk/ai_academic_assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/aadithyaraja1234-cmyk/ai_academic_assistant/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)

AI Academic Assistant is a structured answer generator built with **Streamlit**, **LiteLLM**, and the **Groq API**. It turns any academic question into a validated JSON payload — explanation, worked example, key insights — rendered as a web app or exportable as a PDF, using a clean, layered architecture that separates prompt engineering, LLM interaction, and post-processing from the UI.

---

## 🚀 Live Demo

[Live Application](https://aiacademicassistant-sw2q7zdsxlnkxlsfk4qnpc.streamlit.app/) (Streamlit Community Cloud) · [Hugging Face Space](https://huggingface.co/spaces/aadithya1234/ai-academic-assistant) (landing page with proper link-preview/OG metadata)

---

## 🧠 Features

- Schema-constrained, structured answers (explanation, example, key insights), validated with Pydantic
- Robust JSON parsing that survives markdown fences / stray prose around the payload, with a graceful unstructured fallback instead of crashing
- Retry with backoff on transient LLM API failures
- Per-response latency and token-usage tracking, surfaced in the UI
- PDF export of any answer
- CLI entry point for running the pipeline without Streamlit
- Automated eval harness that scores structural compliance, completeness, latency, and token cost against a fixed question set
- Input validation (length/emptiness) shared by both entry points, plus structured logging around retries and failures
- 28 unit tests at 99% coverage of `module3`, none requiring an API key (LLM calls are mocked)
- CI on every push/PR: ruff (lint), mypy (types), pytest with coverage
- Secrets kept out of source control (`.env` locally, Streamlit Secrets in production)

---

## 🏗️ Architecture

```
Input → Prompt Layer → LLM Layer (+ retry) → Post-processing (JSON parse + validate) → UI
```

Two interchangeable entry points (`streamlit_app.py` and `cli.py`) drive the same `pipeline.run_pipeline()`, so the prompt/LLM/post-processing logic is fully decoupled from how the question is collected or the answer is displayed. The LLM is instructed to return a JSON object matching the `StructuredAnswer` schema; `post_processing.py` parses and validates it, falling back to a plain-text answer (flagged `is_structured=False`) if the model doesn't comply.

## 📂 Project Structure

```
ai_academic_assistant/
│
├── module3/                    # Core application module
│   ├── streamlit_app.py        # Streamlit web interface (UI layer)
│   ├── cli.py                  # Terminal entry point (no Streamlit needed)
│   ├── input_layer.py          # Stdin input collection for the CLI
│   ├── pipeline.py             # Orchestrates prompt -> LLM -> post-processing
│   ├── prompt_layer.py         # Prompt engineering & system instructions
│   ├── llm_layer.py            # Groq + LiteLLM integration, retries, usage tracking
│   ├── post_processing.py      # JSON extraction & schema validation
│   ├── schemas.py              # Pydantic StructuredAnswer model
│   ├── pdf_export.py           # Renders an answer as a downloadable PDF
│   └── requirements.txt        # Runtime dependencies
│
├── eval/                       # Offline evaluation harness
│   ├── questions.json          # 15-question fixed eval set across 8 subjects
│   ├── run_eval.py             # Scores structural compliance, latency, tokens
│   └── REPORT.md               # Latest committed eval run (see below)
│
├── tests/                      # Unit tests (pytest)
├── conftest.py                 # Makes module3/ importable from tests/
├── pyproject.toml              # ruff / mypy / pytest / coverage config
├── requirements-dev.txt        # Runtime + test + lint/type-check dependencies
├── .github/workflows/ci.yml    # Lint + type-check + test on every push/PR
├── .env.example                # Template for local environment variables
├── .gitignore
├── LICENSE
└── README.md
```

## ⚙️ Tech Stack

- Python 3.10+
- Streamlit
- LiteLLM
- Groq API
- Pydantic
- fpdf2
- pytest, pytest-cov
- ruff, mypy
- GitHub Actions (CI)

---

## 🛠️ Local Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/aadithyaraja1234-cmyk/ai_academic_assistant.git
cd ai_academic_assistant
```

### 2️⃣ Install dependencies

```bash
pip install -r module3/requirements.txt
```

### 3️⃣ Configure environment variables

Copy the example file and fill in your own Groq API key:

```bash
cp .env.example module3/.env
```

```
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=groq/openai/gpt-oss-20b
```

### 4️⃣ Run the app

```bash
cd module3
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`.

Alternatively, run it from the terminal without Streamlit:

```bash
cd module3
python cli.py
```

---

## ✅ Testing

```bash
pip install -r requirements-dev.txt
pytest
```

The suite covers prompt construction and input validation, JSON extraction/parsing (including malformed-output and non-object fallbacks), the pipeline's wiring and metadata, retry behavior on transient API errors, the CLI's error handling, and PDF export — all with the LLM call mocked, so it runs for free without an API key. Currently 28 tests, 99% line coverage of `module3`.

### Code quality

```bash
ruff check .        # lint
mypy module3         # static type checking
pytest --cov --cov-report=term-missing   # tests + coverage report
```

All three run in [CI](.github/workflows/ci.yml) on every push and pull request against Python 3.11 and 3.12; config lives in [pyproject.toml](pyproject.toml).

## 📊 Evaluation

`eval/run_eval.py` runs the assistant against a fixed 15-question set spanning 8 subjects (physics, biology, chemistry, math, CS, economics, history, statistics) and reports:

- **Structured-output rate** — % of responses that parse as valid JSON matching the schema
- **Completeness rate** — % of responses where explanation, example, and key insights are all non-empty
- **Latency** — median / max response time
- **Token usage** — median total tokens per response

This makes real, billed calls to the Groq API, so it requires `GROQ_API_KEY` to be set (see above) and is kept separate from the free/mocked pytest suite:

```bash
python eval/run_eval.py
```

Results are written to `eval/results.json` (raw) and `eval/REPORT.md` (summary table). The committed [eval/REPORT.md](eval/REPORT.md) reflects the most recent run: **100% structured-output rate, 100% completeness, 0 failed calls across 15 questions** (median latency 1.2s, median 544 tokens/response) on `groq/openai/gpt-oss-20b`.

---

## 🌐 Deployment (Streamlit Cloud)

1. Push your project to GitHub
2. Go to https://share.streamlit.io
3. Click **New App** and select this repository
4. Set the main file path to `module3/streamlit_app.py`
5. Add secrets in Advanced Settings:

   ```
   GROQ_API_KEY = "your_actual_key_here"
   MODEL_NAME = "groq/openai/gpt-oss-20b"
   ```

6. Deploy

---

## 🔐 Security

- API keys are never committed — `.env` is gitignored, and only `.env.example` is tracked
- The LLM layer reads credentials from environment variables first and falls back to Streamlit Secrets, so it never depends on `st.secrets` being available (e.g. when imported by tests, the CLI, or the eval harness)
- Production secrets are stored securely using Streamlit Secrets

---

## 🎯 Use Cases

- Academic learning and exam preparation
- Concept explanation and structured summaries
- Demonstrating a small, testable, evaluated LLM application architecture

---

## ✅ Launch Checklist

[LAUNCH_CHECKLIST.md](LAUNCH_CHECKLIST.md) walks through the standard site-readiness checklist (meta tags, mobile, forms, privacy, SEO, etc.) item by item against this app, including what's genuinely done, what doesn't apply to a single-page tool, and what's blocked by Streamlit Community Cloud's hosting model (no custom `<head>`, no static file root).

---

## 📈 Future Improvements

- Chat-style conversational interface with memory
- Streaming token output
- LLM-as-judge scoring in the eval harness (answer correctness, not just structure)
- Authentication and usage tracking

---

## 👨‍💻 Author

**Aadithya Raja Anil**

---

## 📄 License

Released under the [MIT License](LICENSE).
