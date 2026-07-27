import pdfplumber
import docx
from openai import OpenAI
import json


# OpenAI API Key
API_KEY = "YOUR_OPENAI_API_KEY"

client = OpenAI(
    api_key=API_KEY
)


def extract_text(uploaded_file):

    text = ""

    if uploaded_file.name.endswith(".pdf"):

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:
                data = page.extract_text()

                if data:
                    text += data + "\n"


    elif uploaded_file.name.endswith(".docx"):

        doc = docx.Document(uploaded_file)

        for para in doc.paragraphs:
            text += para.text + "\n"


    return text



def evaluate_assignment(text):

    prompt = f"""

You are a university professor.

Evaluate this student assignment.

Give marks:

1. Understanding - 20
2. Technical Accuracy - 20
3. Examples - 20
4. Originality - 20
5. Presentation - 20

Return only JSON:

{{
"understanding":0,
"technical":0,
"examples":0,
"originality":0,
"presentation":0,
"total":0,
"status":"",
"feedback":""
}}

Assignment:

{text}

"""


    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]

    )


    result = response.choices[0].message.content

    return json.loads(result)
