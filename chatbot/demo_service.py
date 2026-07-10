import sqlite3
from database.database import DATABASE_NAME


def save_demo(name, company, email, phone, product, preferred_datetime):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO demo_requests
        (name, company, email, phone, product, preferred_datetime)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            company,
            email,
            phone,
            product,
            preferred_datetime,
        ),
    )

    conn.commit()
    conn.close()

    return True
