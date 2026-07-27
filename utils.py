import streamlit as st
import pdfplumber
import docx
import json
import google.generativeai as genai


# Gemini API Setup

try:
    api_key = st.secrets["GOOGLE_API_KEY"]

except Exception:
    st.error("GOOGLE_API_KEY missing in Streamlit Secrets")
    st.stop()


genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "gemini-1.5-pro"
)


# Extract PDF / DOCX text

def extract_text(uploaded_file):

    if uploaded_file.name.endswith(".pdf"):

        text = ""

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text


    elif uploaded_file.name.endswith(".docx"):

        doc = docx.Document(uploaded_file)

        text = ""

        for para in doc.paragraphs:
            text += para.text + "\n"

        return text


    return ""


# AI Evaluation

def evaluate_assignment(text):

    prompt = f"""

You are a university professor.

Evaluate this assignment.

Give marks:

Understanding /20
Technical Accuracy /20
Critical Thinking /20
Images /20
Presentation /20

Return JSON only.

Format:

{{
"understanding":0,
"technical":0,
"critical":0,
"images":0,
"presentation":0,
"total":0,
"status":"",
"feedback":""
}}

Assignment:

{text}

"""


    response = model.generate_content(prompt)


    result = json.loads(response.text)


    return result
