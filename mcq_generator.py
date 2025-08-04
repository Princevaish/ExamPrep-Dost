import os
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fpdf import FPDF
from llm_config import llm

# Set output directory
OUTPUT_DIR = r"E:\\ExamPrepPDFs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Prompt for MCQ generation
prompt_mcq = PromptTemplate(
    template=(
        "You are a helpful assistant who generates MCQs with perfect formatting.\n"
        "Generate {num_ques} multiple-choice questions on the topic: {user_input}.\n\n"
        "Format STRICTLY like this:\n"
        "1. Question text?\n"
        "A. Option A\n"
        "B. Option B\n"
        "C. Option C\n"
        "D. Option D\n\n"
        "Include the correct answer after each question in this format:\n"
        "Answer: Option Letter (e.g., A, B, C, or D)\n\n"
        "Leave a blank line between each question.\n"
        "Start now:"
    ),
    input_variables=["user_input", "num_ques"]
)

# Parser
parser = StrOutputParser()
mcq_chain = prompt_mcq | llm | parser

# Styled PDF Generator for MCQs with answer key
def generate_styled_mcq_pdf(mcq_text: str, title: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, f"{title} - MCQs", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)

    questions = []
    answers = []

    parts = mcq_text.strip().split("\n\n")
    parts = [part for part in parts if not part.lower().startswith("here are 30 multiple-choice questions")]

    for part in parts:
        lines = part.strip().split("\n")
        question_block = []
        answer = None
        for line in lines:
            if line.strip().lower().startswith("answer:"):
                answer = line.strip().split(":")[1].strip()
            else:
                question_block.append(line)
        if question_block:
            questions.append(question_block)
        if answer:
            answers.append(answer)

    for block in questions:
        for line in block:
            pdf.multi_cell(0, 8, line)
        pdf.ln(5)

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Answer Key", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    for idx, answer in enumerate(answers, start=1):
        pdf.cell(0, 8, f"Q{idx}: {answer}", ln=True)

    pdf_output = os.path.join(OUTPUT_DIR, f"{title}_mcqs.pdf")
    pdf.output(pdf_output)
    with open(pdf_output, "rb") as file:
        return file.read()

# ✅ New function to generate MCQs using the LLM chain
def generate_mcqs(user_input: str, num_ques: int) -> str:
    return mcq_chain.invoke({'user_input': user_input, 'num_ques': num_ques})
