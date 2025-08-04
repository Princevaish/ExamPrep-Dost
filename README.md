# ExamPrep Dost 🎓🧠

**ExamPrep Dost** is an AI-powered study companion that generates high-quality **MCQs**, **summaries**, and **full tutorials** from any academic topic. It is designed for students, educators, and competitive exam aspirants who want to learn smarter and revise faster — powered by **LangChain**, **LLaMA models**, and **Groq’s blazing-fast inference API**.

---

## 🚀 Features

- 🔹 **MCQ Generator**: Create well-structured multiple-choice questions from any topic.
- 🔹 **Summary Generator**: Get concise, high-yield summaries for quick revision.
- 🔹 **Tutorial Generator**: Automatically generate detailed tutorials with theory + code.
- 🔹 **PDF Export**: All outputs are exported as styled PDFs — ready to share, print, or upload.
- 🔹 **Fast Inference**: Powered by Groq API for ultra-fast LLM responses.

---

## 📂 Folder Structure

Exam_Prep_Dost/
│
├── .env # API keys and environment configs (ignored in git)
├── app.py # Streamlit frontend app
├── generate_mcqs.py # LangChain pipeline for MCQ generation
├── generate_summary.py # Summary generator logic
├── generate_tutorial.py # Tutorial + code example generator
├── llm_config.py # LLM setup (Groq + LangChain)
├── requirements.txt # Python dependencies
└── README.md # This file


---

## 📄 Sample Outputs

### 📘 MCQs on Generative AI
- 30+ MCQs with options and answer key
- Covers model types, challenges, and applications  
**[See Sample →](./generative_ai_mcqs.pdf)**

### 📙 SQL Summary Notes
- Concise definitions and command breakdowns  
**[See Sample →](./Autograd_summary.pdf)**

### 📗 SQL Tutorial
- Full coverage with theory, code examples, interview Qs & DB schema design  
**[See Sample →](./Heaps_and_Tries_tutorial.pdf)**

---

## ⚙️ Tech Stack

- 🧠 **LangChain** for orchestrating LLM pipelines
- 🐎 **LLaMA (via Groq API)** for low-latency inference
- 🧾 **FPDF** for PDF generation
- 🌐 **Streamlit** for interactive UI

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/Princevaish/ExamPrep-Dost.git
cd ExamPrep-Dost

# Create a virtual environment
python -m venv myenv
myenv\Scripts\activate  # (for Windows)

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key in a .env file
echo GROQ_API_KEY=your_key_here > .env

# Run the app
streamlit run app.py
