import sqlite3
from database.database import DATABASE_NAME


def save_ticket(name, company, email, phone, product, issue):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tickets
        (name, company, email, phone, product, issue)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (name, company, email, phone, product, issue),
    )

    conn.commit()
    conn.close()
