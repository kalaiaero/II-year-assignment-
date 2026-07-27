import pdfplumber
import docx
import json
import google.generativeai as genai


# Gemini API Key
API_KEY = "YOUR_GEMINI_API_KEY_HERE"

genai.configure(api_key=API_KEY)


model = genai.GenerativeModel("gemini-1.5-flash")
)


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


def evaluate_assignment(text):

    prompt = f"""

You are a university professor.

Evaluate this student assignment.

Give marks:

Understanding: /20
Technical Accuracy: /20
Critical Thinking: /20
Images: /20
Presentation: /20

Return only JSON:

{{
"understanding":0,
"technical":0,
"critical":0,
"images":0,
"presentation":0,
"total":0,
"status":"Accepted",
"feedback":""
}}

Assignment:

{text}

"""


    response = model.generate_content(prompt)

    result = json.loads(response.text)

    return result
