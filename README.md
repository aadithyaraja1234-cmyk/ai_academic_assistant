# 🎓 AI Academic Assistant

AI Academic Assistant is a structured answer generator built using **Streamlit**, **LiteLLM**, and the **Groq API**. The application provides clear, concise, and structured academic explanations with examples and key insights. It is designed with a clean modular architecture that separates prompt engineering, LLM interaction, and post-processing logic from the user interface.

---

## 🚀 Live Demo

[Live Application](https://aiacademicassistant-sw2q7zdsxlnkxlsfk4qnpc.streamlit.app/)

---

## 🧠 Features

- Structured academic answers  
- Clear explanations  
- Practical examples  
- Key insights section  
- Controlled system prompting  
- Deterministic temperature setting  
- Modular layered architecture  
- Groq LLM integration via LiteLLM  
- Streamlit-based web interface  
- Secure cloud deployment using Streamlit Secrets  

---

## 🏗️ Architecture

The application follows a clean layered pipeline:

Input → Prompt Layer → LLM Layer → Post Processing → UI

## 📂 Project Structure

```
ai_academic_assistant/
│
├── module3/                          # Core application module
│   │
│   ├── streamlit_app.py              # Streamlit web interface (UI layer)
│   ├── pipeline.py                   # Application orchestration logic
│   ├── prompt_layer.py               # Prompt engineering & system instructions
│   ├── llm_layer.py                  # Groq + LiteLLM integration layer
│   ├── post_processing.py            # Output formatting & cleaning
│   └── requirements.txt              # Python dependencies
│
├── .env                              # Local environment variables (excluded from Git)
├── .gitignore                        # Git ignore configuration
└── README.md                         # Project documentation
```

## ⚙️ Tech Stack

- Python 3.10+
- Streamlit
- LiteLLM
- Groq API
- Streamlit Cloud

---

## 🛠️ Local Installation

### 1️⃣ Clone the repository
git clone https://github.com/your-username/ai_academic_assistant.git

cd ai_academic_assistant/module3

### 2️⃣ Install dependencies
pip install -r requirements.txt

### 3️⃣ Create a `.env` file (for local development only)
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=groq/llama-3.1-8b-instant


### 4️⃣ Run the app
streamlit run streamlit_app.py


The app will open at:
http://localhost:8501


---

## 🌐 Deployment (Streamlit Cloud)

1. Push your project to GitHub  
2. Go to https://share.streamlit.io  
3. Click **New App** and select your repository  
4. Set the main file path (example: `module3/streamlit_app.py`)  
5. Add secrets in Advanced Settings:

GROQ_API_KEY = "your_actual_key_here"
MODEL_NAME = "groq/llama-3.1-8b-instant"


6. Deploy  

---

## 🔐 Security

- API keys are not stored in the repository  
- `.env` file is excluded from version control  
- Production secrets are stored securely using Streamlit Secrets  

---

## 🎯 Use Cases

- Academic learning  
- Concept explanation  
- Exam preparation  
- Structured summaries  
- AI demo applications  
- Portfolio projects  

---

## 📈 Future Improvements

- Strict JSON structured output  
- PDF export  
- Chat-style conversational interface  
- Streaming token output  
- Authentication system  
- Usage tracking and analytics  

---

## 👨‍💻 Author

**Aadithya Raja Anil**

---

## ⭐ Support

If you found this project useful:

- ⭐ Star the repository  
- 🍴 Fork and improve it  
- 📢 Share with others  
