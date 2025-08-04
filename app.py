# =======================
# app.py (Main Streamlit Entry Point)
# =======================
import streamlit as st
from mcq_generator import generate_mcqs, generate_styled_mcq_pdf
from summary_generator import generate_summary_pdf, get_summary_for_topic
from tutorial_generator import generate_tutorial_pdf, tutorial_chain

# Common topics dropdown
COMMON_TOPICS = [
    "Linear Regression", "Decision Trees", "Neural Networks",
    "Operating Systems", "Database Management", "Computer Networks",
    "Software Engineering", "OOPs in Java", "Cloud Computing"
]

st.set_page_config(page_title="ExamPrep Dost", layout="centered")
st.title("📘 ExamPrep Dost")
st.caption("Your AI-powered assistant to generate MCQs, summaries, and full tutorials with code & interview prep!")

# === MCQ Generator ===
with st.expander("📝 Generate MCQs", expanded=True):
    with st.form("mcq_form"):
        user_input = st.selectbox("Select or type a topic:", ["--Type your own--"] + COMMON_TOPICS)
        if user_input == "--Type your own--":
            user_input = st.text_input("Enter custom topic")
        num_ques = st.slider("Number of MCQs", min_value=1, max_value=50, value=10)
        mcq_submit = st.form_submit_button("Generate MCQs")

    if mcq_submit and user_input:
        mcqs = generate_mcqs(user_input, num_ques)
        st.success("MCQs Generated!")
        st.code(mcqs)
        mcq_pdf = generate_styled_mcq_pdf(mcqs, user_input)
        st.download_button("📥 Download MCQ PDF", data=mcq_pdf, file_name=f"{user_input}_mcqs.pdf", mime="application/pdf")

# === Summary Generator ===
with st.expander("🧠 Generate Summary", expanded=False):
    with st.form("summary_form"):
        sum_input = st.selectbox("Select or type a topic:", ["--Type your own--"] + COMMON_TOPICS)
        if sum_input == "--Type your own--":
            sum_input = st.text_input("Enter custom topic for summary")
        sum_submit = st.form_submit_button("Generate Summary")

    if sum_submit and sum_input:
        summary_text = get_summary_for_topic(sum_input)
        st.success("Summary Generated!")
        st.text_area("Summary", summary_text, height=300)
        summary_pdf = generate_summary_pdf(summary_text, sum_input)
        st.download_button("📥 Download Summary PDF", data=summary_pdf, file_name=f"{sum_input}_summary.pdf", mime="application/pdf")

# === Tutorial Generator ===
with st.expander("📘 Generate Full Tutorial", expanded=False):
    with st.form("tutorial_form"):
        tut_input = st.selectbox("Select or type a topic:", ["--Type your own--"] + COMMON_TOPICS)
        if tut_input == "--Type your own--":
            tut_input = st.text_input("Enter custom topic for tutorial")
        tut_submit = st.form_submit_button("Generate Tutorial")

    if tut_submit and tut_input:
        tutorial_text = tutorial_chain.invoke({"topic": tut_input})
        st.success("Tutorial Generated!")
        st.text_area("Tutorial Preview", tutorial_text[:1500] + "...", height=300)
        tutorial_pdf = generate_tutorial_pdf(tutorial_text, tut_input)
        st.download_button("📘 Download Tutorial PDF", data=tutorial_pdf, file_name=f"{tut_input}_tutorial.pdf", mime="application/pdf")

st.markdown(
    "<hr style='margin-top: 40px; margin-bottom: 10px;'>",
    unsafe_allow_html=True
)

st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "🔧 Built with ❤️ using <b>LangChain</b>, <b>LLaMA 3</b>, and <b>Streamlit</b>"
    "</div>",
    unsafe_allow_html=True
)
