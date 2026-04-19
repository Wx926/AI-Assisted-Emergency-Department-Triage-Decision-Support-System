import joblib
import os
import pandas as pd

# Load trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "triage_model.pkl")
model = joblib.load(MODEL_PATH)

# Risk scores per class
RISK_SCORES = {
    "Critical": 92,
    "Urgent": 65,
    "Normal": 20
}

# Reasons per class
REASONS = {
    "Critical": "Low oxygen saturation and/or chest pain with unstable vitals detected.",
    "Urgent": "Elevated heart rate and/or fever with moderate risk indicators.",
    "Normal": "Vitals within acceptable range. No severe symptoms detected."
}

def predict_triage(data: dict) -> dict:
    """
    Input: patient data dict
    Output: severity, risk score, reason, method
    """

    # --- RULE-BASED SAFETY NET (hard rules first) ---
    if data["spo2"] < 90 or (data["chest_pain"] == 1 and data["heart_rate"] > 110):
        return {
            "severity": "Critical",
            "risk_score": 95,
            "reason": "RULE TRIGGERED: SpO2 below 90% or chest pain with high heart rate.",
            "method": "rule-based"
        }

    # --- ML MODEL PREDICTION ---
    features = pd.DataFrame([{
            "age":                  data["age"],
            "heart_rate":           data["heart_rate"],
            "spo2":                 data["spo2"],
            "temperature":          data["temperature"],
            "pain_score":           data["pain_score"],
            "chest_pain":           data["chest_pain"],
            "fever":                data["fever"],
            "headache":             data["headache"],
            "shortness_of_breath":  data["shortness_of_breath"]
        }])

    prediction = model.predict(features)[0]

    return {
        "severity": prediction,
        "risk_score": RISK_SCORES[prediction],
        "reason": REASONS[prediction],
        "method": "ml-model"
    }