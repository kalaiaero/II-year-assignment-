import streamlit as st
import pdfplumber
from PIL import Image
import tempfile
import os
from transformers import pipeline

st.title("Assignment Evaluation System")

# AI Image Detector
detector = pipeline(
    "image-classification",
    model="umm-maybe/AI-image-detector"
)

uploaded_file = st.file_uploader(
    "Upload Assignment",
    type=["pdf","docx"]
)

if uploaded_file:

    st.success("File Uploaded")

    images=[]

    if uploaded_file.name.endswith(".pdf"):

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                for img in page.images:

                    x0,y0,x1,y1 = img["x0"],img["top"],img["x1"],img["bottom"]

                    crop = page.crop((x0,y0,x1,y1))

                    im = crop.to_image(resolution=200)

                    temp = tempfile.NamedTemporaryFile(delete=False,suffix=".png")

                    im.save(temp.name)

                    images.append(temp.name)

    ai_found=False

    for image in images:

        result=detector(image)

        label=result[0]["label"]

        score=result[0]["score"]

        st.write(label,score)

        if "AI" in label.upper() and score>0.80:
            ai_found=True

    if ai_found:

        st.error("Assignment Rejected")

        st.write("Reason: AI-generated image detected.")

    else:

        st.success("Original Images Found")

        marks=0

        text=""

        if uploaded_file.name.endswith(".pdf"):

            with pdfplumber.open(uploaded_file) as pdf:

                for page in pdf.pages:

                    text+=page.extract_text() or ""

        words=len(text.split())

        if words>1000:
            marks+=20

        elif words>700:
            marks+=15

        else:
            marks+=10

        if len(images)>=3:
            marks+=20

        elif len(images)>=2:
            marks+=15

        else:
            marks+=10

        marks+=60

        st.success(f"Final Marks : {marks}/100")
