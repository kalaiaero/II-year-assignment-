import sqlite3
import os

DB_NAME = "assignment.db"


def get_connection():
    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )


def create_table():

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS assignments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            register_number TEXT,
            department TEXT,
            subject TEXT,
            marks INTEGER,
            status TEXT,
            feedback TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_result(
    student_name,
    register_number,
    department,
    subject,
    marks,
    status,
    feedback
):

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO assignments
        (
            student_name,
            register_number,
            department,
            subject,
            marks,
            status,
            feedback
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        student_name,
        register_number,
        department,
        subject,
        marks,
        status,
        feedback
    ))

    conn.commit()
    conn.close()



def view_all():

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT * FROM assignments"
    )

    data = c.fetchall()

    conn.close()

    return data



def search_student(regno):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT * FROM assignments WHERE register_number=?",
        (regno,)
    )

    data = c.fetchall()

    conn.close()

    return data
