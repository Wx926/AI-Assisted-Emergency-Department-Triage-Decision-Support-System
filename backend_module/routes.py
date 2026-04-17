from fastapi import APIRouter
from pydantic import BaseModel
from database import get_connection
from datetime import datetime

router = APIRouter()


class PatientInput(BaseModel):
    name: str
    age: int
    heart_rate: int
    oxygen_level: int
    blood_pressure: str
    symptom: str


# DOOR1: receive a new patient
@router.post("/patients")
def add_patient(data: PatientInput):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
                   INSERT INTO patients (name, age, heart_rate, oxygen_level, blood_pressure, symptom)
                   VALUES (?,?,?,?,?,?)
                     """,
        (
            data.name,
            data.age,
            data.heart_rate,
            data.oxygen_level,
            data.blood_pressure,
            data.symptom,
        ),
    )

    conn.commit()
    patient_id = cursor.lastrowid
    conn.close()

    return {"message": "Patient added successfully", "patient_id": patient_id}


# DOOR2: Run triage on a patient
@router.post("/triage/{patient_id}")
def run_triage(patient_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()

    if not patient:
        return {"error": "Patient not found"}

    # Placeholder triage logic
    result = {
        "severity": "Critical",
        "risk_score": 92,
        "reason": "Placeholder - AI model not connected yet",
    }

    cursor.execute(
        """
                    INSERT INTO triage_results(patient_id, severity, risk_score, reason)
                    VALUES (?,?,?,?)
                    """,
        (patient_id, result["severity"], result["risk_score"], result["reason"]),
    )

    cursor.execute(
        """
                   INSERT INTO queue (patient_id, severity)
                   VALUES (?,?)
                   """,
        (patient_id, result["severity"]),
    )

    if result["severity"] == "Critical":
        cursor.execute(
            """
                        INSERT INTO alerts (patient_id, message)
                        VALUES (?,?)
                        """,
            (
                patient_id,
                f"CRITICAL ALERT: Patient {patient['name']} needs immediate attention!",
            ),
        )
        conn.commit()
        conn.close()

        return {
            "message": "Triage completed",
            "patient_id": patient_id,
            "result": result,
        }

    # DOOR3 - Get the patient queue


@router.get("/queue")
def get_queue():
    conn = get_connection()
    curosr = conn.cursor()
    cursor.execute(
        """
        SELECT q.id, p.name, p.age, q.severity, q.status, q.timestamp
        FROM queue q
        JOIN patients p ON q.patient_id = p.id
        WHERE q.status = 'waiting'
        ORDER BY CASE q.severity
            WHEN 'Critical' THEN 1
            WHEN 'Urgent' THEN 2
            WHEN 'Normal' THEN 3
        END
    """
    )
    queue = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {"queue": queue}


@router.get("/alerts")
def get_alerts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT a.id, p.name, a.message, a.timestamp
        FROM alerts a
        JOIN patients p ON a.patient_id = p.id
        WHERE a.is_resolved = 0

    """
    )
    alerts = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {"alerts": alerts}
