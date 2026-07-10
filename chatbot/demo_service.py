import sqlite3

def save_demo(name, company, email, phone, product, preferred_datetime):

    conn = sqlite3.connect("database/tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO demo_requests
        (name, company, email, phone, product, preferred_datetime)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        company,
        email,
        phone,
        product,
        preferred_datetime
    ))

    conn.commit()
    conn.close()

    return True