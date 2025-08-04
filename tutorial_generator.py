import os
from datetime import datetime
from fpdf import FPDF
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_config import llm

OUTPUT_DIR = r"E:\\ExamPrepPDFs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
prompt_tutorial = PromptTemplate(
    input_variables=["topic"],
    template=(
        "You are a professional computer science educator and technical content writer.\n"
        "Create a comprehensive, well-formatted tutorial on the topic: '{topic}'.\n\n"
        "Your tutorial must be rich and detailed enough to span **at least 15 A4 pages** when converted to PDF.\n"
        "Use markdown-style formatting with `#`, `##`, `###` for headings and triple backticks for code blocks.\n\n"
        "Structure the tutorial as follows:\n\n"
        "1. **Introduction and Importance**\n"
        "   - Briefly define the topic.\n"
        "   - Explain why it is significant in both academic and real-world scenarios.\n"
        "   - List real-world use cases and applications.\n\n"
        "2. **Major Subtopics**\n"
        "   - List and explain 5–7 fundamental subtopics.\n"
        "   - For each subtopic:\n"
        "     • Explain the theory.\n"
        "     • Provide commented, practical code examples in the most relevant programming language.\n\n"
        "3. **Advanced Concepts**\n"
        "   - List and explain 3–5 advanced subtopics.\n"
        "   - Include real-world relevance and clean, well-commented code examples.\n\n"
        "4. **Medium-Level Practice Questions**\n"
        "   - Provide at least 5 medium-difficulty coding or conceptual questions.\n"
        "   - For each question:\n"
        "     • State the full question clearly.\n"
        "     • Provide a thorough, multi-paragraph explanation of the solution.\n"
        "     • Include step-by-step reasoning.\n"
        "     • Add clean, well-commented code examples.\n\n"
        "5. **Advanced-Level Questions**\n"
        "   - Provide at least 5 advanced-level coding/design questions.\n"
        "   - For each question:\n"
        "     • Explain the problem clearly.\n"
        "     • Give a detailed, multi-step explanation of the logic.\n"
        "     • Provide optimized, clean code with comments.\n\n"
        "6. **Top 20 Interview Questions and Answers**\n"
        "   - List 20 commonly asked interview questions related to this topic.\n"
        "   - For each question:\n"
        "     • Write a **detailed and helpful answer**, ideally 2-3 paragraphs.\n"
        "     • Include examples, real-world context, and use bullet points if helpful.\n"
        "     • Add relevant code snippets using triple backticks and comments.\n"
        "     • Do **not** write just 'Answer:' — each response must be fully explained and technically sound.\n\n"
        "7. **Conclusion and Summary**\n"
        "   - Recap key concepts.\n"
        "   - Share best practices, common mistakes, and pro tips.\n"
        "   - Suggest next steps for further learning or exploration.\n\n"
        "Formatting Rules:\n"
        "- Use markdown formatting with appropriate heading levels (.).\n"
        "- Use triple backticks for all code blocks and comment each part.\n"
        "- Make content educational, beginner-friendly, and technically rich.\n"
        "- Ensure total content is verbose and spans at least 10 pages in PDF form."
    )
)
parser = StrOutputParser()
tutorial_chain = prompt_tutorial | llm | parser

class TutorialPDF(FPDF):
    def __init__(self, title, author):
        super().__init__()
        self.title = title
        self.author = author

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100)
        self.cell(0, 10, self.title, align="C", ln=True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def chapter_title(self, title):
        clean_title = title.strip().replace("**", "").title()
        self.set_fill_color(36, 74, 104)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, f" {clean_title}", ln=True, fill=True)
        self.ln(3)

    def code_block(self, code):
        self.set_font("Courier", size=10)
        self.set_fill_color(245, 245, 245)
        self.set_text_color(33, 37, 41)
        for line in code.strip().split("\n"):
            self.multi_cell(0, 5, f" {line}", border=0, fill=True)
        self.ln(2)

    def normal_text(self, text):
        clean_text = text.replace("**", "").strip()
        self.set_font("Helvetica", size=11)
        self.set_text_color(0, 0, 0)
        for line in clean_text.split("\n"):
            self.multi_cell(0, 6, line.strip())
        self.ln(2)

    def tip_box(self, tip):
        self.set_font("Helvetica", "I", 10)
        self.set_fill_color(255, 255, 204)
        self.set_text_color(102, 51, 0)
        self.multi_cell(0, 6, f"TIP: {tip.strip().replace('**', '')}", border=1, fill=True)
        self.ln(2)

    def add_metadata(self):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(0)
        self.cell(0, 10, f"Author: {self.author} | Date: {datetime.now().strftime('%B %d, %Y')}", ln=True, align="L")
        self.ln(5)

def generate_tutorial_pdf(tutorial_text: str, topic: str, author: str = "Prince Vaish") -> bytes:
    pdf = TutorialPDF(title=topic.upper(), author=author)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"{topic.upper()} - COMPREHENSIVE TUTORIAL", ln=True, align="C")
    pdf.ln(8)
    pdf.add_metadata()

    in_code_block = False
    code_buffer = []

    for line in tutorial_text.split("\n"):
        line = line.strip()
        if line.startswith("```"):
            in_code_block = not in_code_block
            if not in_code_block and code_buffer:
                pdf.code_block("\n".join(code_buffer))
                code_buffer = []
        elif in_code_block:
            code_buffer.append(line)
        elif line.lower().startswith("tip:"):
            pdf.tip_box(line.split("tip:", 1)[-1])
        elif line.endswith(":") and len(line) < 80:
            pdf.chapter_title(line.replace("**", "").replace(":", ""))
        elif line:
            pdf.normal_text(line)

    output_path = os.path.join(OUTPUT_DIR, f"{topic}_tutorial_cleaned.pdf")
    pdf.output(output_path)
    with open(output_path, "rb") as f:
        return f.read()
