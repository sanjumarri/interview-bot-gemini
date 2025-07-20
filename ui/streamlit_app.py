# ui/streamlit_app.py

import sys
import os
from fpdf import FPDF
import re
import pdfplumber
from unidecode import unidecode

# Add project root to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, ROOT_DIR)

import streamlit as st
from agents.job_role_agent import JobRoleAgent
from acp.router import send_message
from llm.gemini_client import get_feedback_on_answer
import json

ANSWERS_FILE = os.path.join(ROOT_DIR, "session_answers.json")

def save_answers():
    answers = {k: v for k, v in st.session_state.items() if k.endswith("_answer_1") or "_answer_" in k}
    with open(ANSWERS_FILE, "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=2)

def load_answers():
    if os.path.exists(ANSWERS_FILE):
        with open(ANSWERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for k, v in data.items():
                st.session_state[k] = v

# ---- Streamlit Config ----
st.set_page_config(page_title="AI Interview Assistant", layout="centered")
st.title("🤖 AI Interview Preparation Assistant")

load_answers()

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
if "job_role" not in st.session_state:
    st.session_state.job_role = ""
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Beginner"
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# ---- UI Inputs ---



if not st.session_state.interview_started:
    job_role = st.text_input("Enter the job role you're preparing for:", "").title()
    difficulty = st.selectbox("Select difficulty level:", ["Beginner", "Intermediate", "Expert"])

    st.subheader("📄 Upload your Resume (Optional)")
    uploaded_resume = st.file_uploader("Upload your resume (PDF):", type="pdf")

    resume_text = ""
    if uploaded_resume:
        with pdfplumber.open(uploaded_resume) as pdf:
            for page in pdf.pages:
                resume_text += page.extract_text() + "\n"
        st.success("✅ Resume uploaded and parsed!")

    if st.button("Start Interview Preparation"):
        if job_role.strip() == "":
            st.warning("Please enter a job role.")
        else:
            st.session_state.job_role = job_role
            st.session_state.difficulty = difficulty
            st.session_state.resume_text = resume_text
            st.session_state.interview_started = True
            st.rerun()

# ---- Global Questions Dict for PDF ----


# ---- Generate PDF Function ----
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for section, questions in data.items():
        # Section heading
        pdf.set_font("Arial", 'B', size=14)
        pdf.cell(200, 10, txt=unidecode(section), ln=True)  # Clean section title

        # Clean and filter out short questions
        pdf.set_font("Arial", size=12)
        question_num = 1
        for q in questions:
            # Remove prefixes like "Q1:", "1.", "2)" etc.
            q_clean = re.sub(r"^\s*Q?\d+[:\.\)\-]*\s*", "", q).strip()
            q_clean = unidecode(q_clean)  # Clean encoding issues

            if len(q_clean) > 10:
                pdf.multi_cell(0, 10, txt=f"Q{question_num}: {q_clean}")
                question_num += 1

        pdf.ln()

    return pdf.output(dest='S').encode('latin1')  # Now safe to use latin1
# ---- Main Button ----
if st.session_state.interview_started:
    show_feedback = st.checkbox("🧪 Show Feedback & Score for Each Answer", value=False)
    show_followups = st.checkbox("🧩 Generate Follow-Up Questions", value=False)
    show_history = st.checkbox("📜 Show Chat History (Q/A/Feedback)", value=False)
    st.success(f"Interview preparation started for: {st.session_state.job_role}")

    st.markdown(f"🎯 Difficulty Level: **{st.session_state.difficulty}**")
    if st.session_state.resume_text:
        st.markdown("📎 Resume Uploaded: ✅")
    else:
        st.markdown("📎 Resume Uploaded: ❌")
    
    show_coding = st.checkbox("💻 Show Coding Questions", value=True)
    show_hr = st.checkbox("🧠 Show HR Questions", value=True)

    agent = JobRoleAgent(st.session_state.job_role, st.session_state.difficulty)
    messages = agent.analyze_role()

    questions_dict = {}

    with st.spinner("Generating interview questions..."):
        for msg in messages:
            result = send_message(msg, st.session_state.resume_text)

            if result and isinstance(result, list):
                # Determine section type
                if msg['receiver'] == 'CodingAgent':
                    if "no coding" in result[0].lower():
                        st.subheader("💻 Coding Questions: Not required for this role.")
                        continue  # This continue is safe (we are inside the outer `for` loop)
                    st.subheader("💻 Coding Questions:")
                    st.markdown("---")
                    section_key = "Coding Questions"
                    key_prefix = "coding"

                elif msg['receiver'] == 'HRAgent':
                    if "no hr" in result[0].lower():
                        st.subheader("🧠 HR Questions: Not required for this role.")
                        continue
                    st.subheader("🧠 HR Questions:")
                    st.markdown("---")
                    section_key = "HR Questions"
                    key_prefix = "hr"

                else:
                    continue  # Just in case unknown message type

                    # Store for PDF
                questions_dict[section_key] = result

                    # Clean and dedupe questions
                cleaned_questions = [q.strip("•*- \n") for q in result if len(q.strip()) > 10]
                deduped = []
                for q in cleaned_questions:
                    q = re.sub(r"^\d+[\.\):\- ]+", "", q).strip()

                    if '?' in q:
                        q = q.split('?')[0].strip() + '?'
                    deduped.append(q)

                # Render each question and capture answer
                for i, q in enumerate(deduped, 1):
                    st.markdown(f"**Q{i}:** {q}")
                        
                    answer_key = f"{key_prefix}_answer_{i}"

                    # Load previous answer (if any)
                    default_answer = st.session_state.get(answer_key, "")

                    # Show text area with persisted value
                    user_answer = st.text_area(
                        f"Your answer to Q{i}:", 
                        value=default_answer,
                        key=answer_key
                    )

                    # Optional: re-store after typing
                    if user_answer:
                        st.session_state[answer_key] = user_answer
                        
                        if show_feedback:
                            feedback = get_feedback_on_answer(q, user_answer)
                            st.markdown(f"🧠 **Feedback:** {feedback['suggestion']}")
                            st.markdown(f"📊 **Score:** {feedback['score']}/10")
                            st.session_state[f"{answer_key}_feedback"] = feedback
                        
                        if show_followups:
                            from llm.gemini_client import get_followup_question  # 👈 Add this function (see below)
                            followup = get_followup_question(q, user_answer)
                            st.markdown(f"🔁 **Follow-Up:** {followup}")
                            st.session_state[f"{answer_key}_followup"] = followup

    
    save_answers()            

    st.info("🔄 Agent messages sent. Check logs/communication_log.txt")
    st.markdown("### ✅ Interview Session Complete!")
    st.success("You can now download the questions as PDF or revise your answers.")


        # ---- Download as PDF ----
    if questions_dict:
        pdf_data = generate_pdf(questions_dict)
        st.download_button(
            label="📄 Download as PDF",
            data=pdf_data,
            file_name="interview_questions.pdf",
            mime='application/pdf'
        )

    # ---- Interview Tips ----
    st.markdown("## 🧠 Interview Tips")
    st.markdown("- Be clear and concise with your answers.")
    st.markdown("- Use real examples from past experience.")
    st.markdown("- Practice aloud before the actual interview.")
    st.markdown("- For coding rounds, explain your thought process clearly.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔁 Reset Entire Session"):
            st.session_state.clear()
            if os.path.exists(ANSWERS_FILE):
                os.remove(ANSWERS_FILE)
            st.rerun()

    with col2:
        if st.button("♻️ Clear All Answers Only"):
            for key in list(st.session_state.keys()):
                if "_answer_" in key:
                    del st.session_state[key]
            if os.path.exists(ANSWERS_FILE):
                os.remove(ANSWERS_FILE)
            st.rerun()
   