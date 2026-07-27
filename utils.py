import json
import pdfplumber
import docx
import google.generativeai as genai
import streamlit as st
api_key = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-pro")


def extract_text(uploaded_file):
    """Extract text from PDF or DOCX."""

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
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        return ""


def evaluate_assignment(text):

    prompt = f"""
You are an experienced university professor.

Evaluate the assignment.

Give marks out of 20 for:

1. Understanding
2. Technical Accuracy
3. Critical Thinking
4. Images and Diagrams
5. Presentation

Return ONLY valid JSON.

Example:

{{
  "understanding":18,
  "technical":17,
  "critical":19,
  "images":18,
  "presentation":17,
  "total":89,
  "status":"Accepted",
  "feedback":"Excellent technical explanation. Improve references."
}}

Assignment:

{text}
"""

    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except Exception:
        return {
            "understanding": 0,
            "technical": 0,
            "critical": 0,
            "images": 0,
            "presentation": 0,
            "total": 0,
            "status": "Manual Review",
            "feedback": response.text
        }
