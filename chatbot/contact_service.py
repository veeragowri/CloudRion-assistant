import sqlite3

DATABASE_NAME = "database/tickets.db"


def save_contact(name, company, email, phone, message, product=None):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO contact_inquiries
        (name, company, email, phone, message, product)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (name, company, email, phone, message, product),
    )

    conn.commit()
    conn.close()
