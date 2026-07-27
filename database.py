import sqlite3

# Connect to database
conn = sqlite3.connect("assignment.db", check_same_thread=False)
c = conn.cursor()


def create_table():

    c.execute("""
        CREATE TABLE IF NOT EXISTS assignments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            register_number TEXT UNIQUE,
            department TEXT,
            subject TEXT,
            marks INTEGER,
            status TEXT,
            feedback TEXT
        )
    """)

    conn.commit()


def insert_result(student_name,
                  register_number,
                  department,
                  subject,
                  marks,
                  status,
                  feedback):

    c.execute("""
        INSERT OR REPLACE INTO assignments
        (
            student_name,
            register_number,
            department,
            subject,
            marks,
            status,
            feedback
        )

        VALUES (?,?,?,?,?,?,?)
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


def view_all():

    c.execute("SELECT * FROM assignments")

    return c.fetchall()


def search_student(regno):

    c.execute(
        "SELECT * FROM assignments WHERE register_number=?",
        (regno,)
    )

    return c.fetchall()
