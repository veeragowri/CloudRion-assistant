import sqlite3

DATABASE_NAME = "database/tickets.db"


def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT NOT NULL DEFAULT '',
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            product TEXT NOT NULL,
            issue TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS demo_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            product TEXT NOT NULL,
            preferred_datetime TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contact_inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            message TEXT NOT NULL,
            product TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    _migrate_tickets_table(cursor)

    conn.commit()
    conn.close()

    print("✅ Database created successfully!")


def _migrate_tickets_table(cursor):
    cursor.execute("PRAGMA table_info(tickets)")
    columns = {row[1] for row in cursor.fetchall()}

    if not columns:
        return

    if "priority" in columns:
        cursor.execute(
            """
            CREATE TABLE tickets_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                company TEXT NOT NULL DEFAULT '',
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                product TEXT NOT NULL,
                issue TEXT NOT NULL,
                status TEXT DEFAULT 'Open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            INSERT INTO tickets_new (id, name, company, email, phone, product, issue, status)
            SELECT id, name, COALESCE(company, ''), email, phone, product, issue, status FROM tickets
            """
        )
        cursor.execute("DROP TABLE tickets")
        cursor.execute("ALTER TABLE tickets_new RENAME TO tickets")
    elif "company" not in columns:
        cursor.execute("ALTER TABLE tickets ADD COLUMN company TEXT NOT NULL DEFAULT ''")
