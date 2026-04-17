import sqlite3


def get_connection():
    conn = sqlite3.connect("triage.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            heart_rate INTEGER,
            oxygen_level INTEGER,
            blood_pressure TEXT,
            symptom TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                   )

    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS triage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            severity TEXT,
            risk_score INTEGER,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            severity TEXT,
            status TEXT DEFAULT 'waiting',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            message TEXT,
            is_resolved INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    """
    )
    conn.commit()
    conn.close()
    print("Tables created successfully.")
