from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import PyPDF2
import os
import google.generativeai as genai

# Add a dark network image as background
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://t3.ftcdn.net/jpg/02/13/56/78/360_F_213567841_SiyyM6H4y067caRy58iLulWazeezPaui.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Please set your Gemini API key in a .env file as GEMINI_API_KEY or as an environment variable.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def get_gemini_feedback(resume_text):
    prompt = (
        "You are an ATS (Applicant Tracking System) resume analyzer. "
        "Given the following resume, do the following:\n"
        "1. Give an ATS score out of 100, based on how well it would pass automated resume screening for a typical software engineering job.\n"
        "2. List the key strengths in the resume.\n"
        "3. Suggest specific, actionable improvements to increase the ATS score, focusing on keywords, formatting, and clarity.\n"
        "Resume:\n"
        f"{resume_text}\n"
        "Respond in a clear, structured format."
    )
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

st.title("RAG-Enhanced Resume Scorer for ATS Systems")

uploaded_file = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = uploaded_file.read().decode("utf-8")

    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=200)

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing"):
            feedback = get_gemini_feedback(resume_text)
        st.subheader("ATS Analysis & Suggestions")
        st.markdown(feedback)