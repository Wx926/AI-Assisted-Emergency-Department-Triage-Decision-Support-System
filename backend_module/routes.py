from fastapi import APIRouter
from pydantic import BaseModel
from database import get_connection
import sys
import os

router = APIRouter()


class PatientInput(BaseModel):
    name: str
    age: int
    heart_rate: int
    oxygen_level: int
    blood_pressure: str
    symptom: str


@router.post("/patients")
def add_patient(data: PatientInput):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO patients (name, age, heart_rate, oxygen_level, blood_pressure, symptom)
            VALUES (?, ?, ?, ?, ?, ?)
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
        return {"message": "Patient added successfully", "patient_id": patient_id}
    finally:
        conn.close()


@router.post("/triage/{patient_id}")
def run_triage(patient_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        patient = cursor.fetchone()

        if not patient:
            return {"error": "Patient not found"}

        # ── Person 1 AI Model Integration ──
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "triage_module")))
        from model_logic import predict_triage

        triage_input = {
            "age":                  patient["age"],
            "heart_rate":           patient["heart_rate"],
            "spo2":                 patient["oxygen_level"],
            "temperature":          37.0,
            "pain_score":           5,
            "chest_pain":           1 if "chest pain" in patient["symptom"].lower() else 0,
            "fever":                1 if "fever" in patient["symptom"].lower() else 0,
            "headache":             1 if "headache" in patient["symptom"].lower() else 0,
            "shortness_of_breath":  1 if "breath" in patient["symptom"].lower() else 0
        }

        ai_result = predict_triage(triage_input)
        result = {
            "severity":   ai_result["severity"],
            "risk_score": ai_result["risk_score"],
            "reason":     ai_result["reason"]
        }
        # ───────────────────────────────────

        cursor.execute(
            """
            INSERT INTO triage_results (patient_id, severity, risk_score, reason)
            VALUES (?, ?, ?, ?)
        """,
            (patient_id, result["severity"], result["risk_score"], result["reason"]),
        )

        cursor.execute(
            """
            INSERT INTO queue (patient_id, severity)
            VALUES (?, ?)
        """,
            (patient_id, result["severity"]),
        )

        if result["severity"] == "Critical":
            cursor.execute(
                """
                INSERT INTO alerts (patient_id, message)
                VALUES (?, ?)
            """,
                (
                    patient_id,
                    f"CRITICAL ALERT: Patient {patient['name']} needs immediate attention!",
                ),
            )

        conn.commit()
        return {
            "message": "Triage completed",
            "patient_id": patient_id,
            "result": result,
        }
    finally:
        conn.close()


@router.get("/queue")
def get_queue():
    conn = get_connection()
    try:
        cursor = conn.cursor()
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
        return {"queue": queue}
    finally:
        conn.close()


@router.get("/alerts")
def get_alerts():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT a.id, p.name, a.message, a.is_resolved, a.timestamp
            FROM alerts a
            JOIN patients p ON a.patient_id = p.id
            WHERE a.is_resolved = 0
        """
        )
        alerts = [dict(row) for row in cursor.fetchall()]
        return {"alerts": alerts}
    finally:
        conn.close()
