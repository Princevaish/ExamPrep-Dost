import os
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fpdf import FPDF
from llm_config import llm, llm2

# Set output directory
OUTPUT_DIR = r"E:\\ExamPrepPDFs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Prompt for explanation
prompt_explanation = PromptTemplate(
    template=(
        "You are an expert educational assistant that provides accurate, detailed, and well-structured explanations.\n"
        "Write a comprehensive explanation on the following topic:\n\n"
        "Topic: {user_input}\n\n"
        "Your explanation should include:\n"
        "1. An introduction to the topic.\n"
        "2. Key concepts and definitions.\n"
        "3. Important subtopics or components.\n"
        "4. Use cases or applications (if any).\n"
        "5. A conclusion summarizing the topic."
    ),
    input_variables=["user_input"]
)

prompt_summary = PromptTemplate(
    input_variables=["sum_content"],
    template=(
        "You are an expert at creating concise, high-yield revision notes for interviews.\n\n"
        "Given the following topic content:\n"
        "{sum_content}\n\n"
        "Generate short notes that:\n"
        "1. Are crystal-clear, logically organized, and perfect for quick last-minute interview revision.\n"
        "2. Cover all essential points: definitions, formulas, facts, code patterns, best practices, and key takeaways.\n"
        "3. Use keyword-based headers like:\n"
        "   - Definitions\n"
        "   - Key Concepts\n"
        "   - Syntax/Code Examples\n"
        "   - Common Mistakes\n"
        "   - Best Practices / Tips\n\n"
        "4. Present information using numbered or dash-based bullet points (no markdown or asterisks).\n"
        "5. Be concise and free from fluff — every line should deliver value.\n"
        "6. If code is relevant, include 1–2 line Python/C++/Java-style snippets or syntax references.\n\n"
        "The output must resemble clean, handwritten notes ready for printing or PDF generation.\n"
        "Avoid paragraphs. Focus on clarity, structure, and usefulness."
    )
)


# Chains
parser = StrOutputParser()
explanation_chain = prompt_explanation | llm | parser
summary_chain = prompt_summary | llm2 | parser

# PDF Class
class CustomPDF(FPDF):
    def header_box(self, title):
        self.set_fill_color(255, 153, 51)
        self.set_text_color(255, 255, 255)
        self.set_font("helvetica", "B", 12)
        self.cell(0, 10, title.upper(), ln=True, fill=True)
        self.ln(2)

# Summary PDF Generator
def generate_summary_pdf(summary_text: str, topic: str) -> bytes:
    pdf = CustomPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("helvetica", "B", 15)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(8, 133, 161)
    pdf.cell(0, 10, f"{topic.upper()} - SHORT NOTES", ln=True, align="C")
    pdf.ln(8)

    if ":" not in summary_text:
        pdf.header_box("SUMMARY")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("helvetica", "", 11)
        for line in summary_text.strip().split("\n"):
            clean_line = line.strip().lstrip("-").strip().replace("**", "")
            if clean_line:
                pdf.multi_cell(0, 7, f" {clean_line}")
                pdf.ln(1)
    else:
        lines = summary_text.strip().split("\n")
        if lines and "clean" in lines[0].lower() and "summary" in lines[0].lower():
            lines = lines[1:]
        current_section = "SUMMARY"
        content_buffer = []

        def flush_section():
            if content_buffer:
                pdf.header_box(current_section)
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("helvetica", "", 11)
                for line in content_buffer:
                    clean_line = line.strip().lstrip("-").strip().replace("**", "")
                    if clean_line:
                        pdf.multi_cell(0, 7, f" {clean_line}")
                        pdf.ln(1)

        for line in lines:
            line = line.strip()
            if not line:
                continue
            elif line.endswith(":") and line[:-1].isupper():
                flush_section()
                current_section = line[:-1]
                content_buffer = []
            else:
                content_buffer.append(line)

        flush_section()

    output_path = os.path.join(OUTPUT_DIR, f"{topic}_summary.pdf")
    pdf.output(output_path)
    with open(output_path, "rb") as f:
        pdf_bytes = f.read()

    os.remove(output_path)
    return pdf_bytes

# ✅ Add this function to support summary generation in app.py
def get_summary_for_topic(topic: str) -> str:
    explanation = explanation_chain.invoke({"user_input": topic})
    summary = summary_chain.invoke({"sum_content": explanation})
    return summary
