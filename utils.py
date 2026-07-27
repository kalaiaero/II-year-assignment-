import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-pro")


def evaluate_assignment(text):

    prompt = f"""
You are an experienced university professor.

Evaluate the following student assignment.

Give marks as follows:

1. Understanding of the Topic (20 Marks)

2. Technical Accuracy (20 Marks)

3. Explanation with Examples (20 Marks)

4. Originality and Critical Thinking (20 Marks)

5. Presentation and Organization (20 Marks)

Total = 100 Marks

Return ONLY in this format:

Understanding: xx/20
Technical Accuracy: xx/20
Examples: xx/20
Originality: xx/20
Presentation: xx/20

Total: xx/100

Feedback:
(Write detailed feedback in 200 words.)

Student Assignment:

{text}
"""

    response = model.generate_content(prompt)

    return response.text


st.subheader("Rubric")

col1,col2=st.columns(2)

with col1:

    st.metric(
        "Understanding",
        result["understanding"]
    )

    st.metric(
        "Technical",
        result["technical"]
    )

    st.metric(
        "Critical Thinking",
        result["critical"]
    )

with col2:

    st.metric(
        "Images",
        result["images"]
    )

    st.metric(
        "Presentation",
        result["presentation"]
    )
