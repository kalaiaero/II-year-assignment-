
import streamlit as st
import os
import pandas as pd

from database import *
from utils import extract_text, evaluate_assignment
st.set_page_config(
    page_title="AI Assignment Evaluation System",
    page_icon="🎓",
    layout="wide"
)

create_table()

menu = st.sidebar.selectbox(
    "Select Portal",
    ["Student Submission", "Faculty Dashboard"]
)

###########################################################
# STUDENT SUBMISSION
###########################################################

if menu == "Student Submission":

    st.title("🎓 AI Assignment Submission Portal")

    col1,col2=st.columns(2)

    with col1:
        name=st.text_input("Student Name")

    with col2:
        regno=st.text_input("Register Number")

    department=st.selectbox(
        "Department",
        [
            "CSE",
            "AI&DS",
            "IT",
            "ECE",
            "EEE",
            "MECH",
            "CIVIL"
        ]
    )

    subject=st.text_input("Subject")

    assignment=st.file_uploader(
        "Upload Assignment",
        type=["pdf","docx"]
    )

    if st.button("Submit Assignment"):

        if assignment is None:

            st.error("Please upload assignment.")

        else:

            os.makedirs("uploads",exist_ok=True)

            filepath=os.path.join(
                "uploads",
                assignment.name
            )

            with open(filepath,"wb") as f:
                f.write(assignment.getbuffer())

text = extract_text(assignment)

result = evaluate_assignment(text)

marks = result["total"]
status = result["status"]
feedback = result["feedback"]
insert_result(
    name,
    regno,
    department,
    subject,
    marks,
    status,
    feedback
)

st.success("Assignment Submitted Successfully")

st.metric("Total Marks", f"{marks}/100")

st.subheader("Rubric Evaluation")

col1, col2 = st.columns(2)

with col1:
    st.metric("Understanding", result["understanding"])
    st.metric("Technical", result["technical"])
    st.metric("Critical Thinking", result["critical"])

with col2:
    st.metric("Images", result["images"])
    st.metric("Presentation", result["presentation"])

st.subheader("Faculty Feedback")

st.write(feedback)
            
            insert_result(
                name,
                regno,
                department,
                subject,
                marks,
                status,
                feedback
            )

            st.success("Assignment Submitted Successfully")

            st.metric(
                "Marks",
                f"{marks}/100"
            )

            st.text_area(
                "Feedback",
                feedback,
                height=200
            )

###########################################################
# FACULTY DASHBOARD
###########################################################

else:

    st.title("Faculty Dashboard")

    password=st.text_input(
        "Faculty Password",
        type="password"
    )

    if password=="admin123":

        st.success("Login Successful")

        data=view_all()

        if len(data)>0:

            df=pd.DataFrame(
                data,
                columns=[
                    "ID",
                    "Student Name",
                    "Register Number",
                    "Department",
                    "Subject",
                    "Marks",
                    "Status",
                    "Feedback"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            st.download_button(
                "Download Results",
                df.to_csv(index=False),
                "Assignment_Results.csv",
                "text/csv"
            )

            st.subheader("Search Student")

            reg=st.text_input(
                "Enter Register Number"
            )

            if st.button("Search"):

                result=search_student(reg)

                if result:

                    rdf=pd.DataFrame(
                        result,
                        columns=[
                            "ID",
                            "Student Name",
                            "Register Number",
                            "Department",
                            "Subject",
                            "Marks",
                            "Status",
                            "Feedback"
                        ]
                    )

                    st.dataframe(rdf)

                else:

                    st.warning("No Record Found")


    elif password!="":

        st.error("Wrong Password")

st.subheader("Evaluation")

st.metric("Marks", marks)

st.success(status)

st.write(feedback)
