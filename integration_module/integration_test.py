import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "triage_module")))

from triage_module.model_logic import predict_triage
from queue_manager import add_patient, show_queue
from monitor import show_monitor

patients = [
    {
        "name": "Ahmad",
        "age": 70,
        "heart_rate": 120,
        "spo2": 85,
        "temperature": 37.0,
        "pain_score": 9,
        "chest_pain": 1,
        "fever": 0,
        "headache": 0,
        "shortness_of_breath": 1
    },
    {
        "name": "Siti",
        "age": 30,
        "heart_rate": 105,
        "spo2": 96,
        "temperature": 38.5,
        "pain_score": 5,
        "chest_pain": 0,
        "fever": 1,
        "headache": 0,
        "shortness_of_breath": 0
    },
    {
        "name": "Raj",
        "age": 25,
        "heart_rate": 75,
        "spo2": 98,
        "temperature": 36.8,
        "pain_score": 2,
        "chest_pain": 0,
        "fever": 0,
        "headache": 1,
        "shortness_of_breath": 0
    }
]

print("\n===== TRIAGEPULSE INTEGRATION TEST =====")

for p in patients:
    result = predict_triage(p)
    add_patient(p, result["severity"])
    print(f"\nPatient : {p['name']}")
    print(f"Severity: {result['severity']}")
    print(f"Risk    : {result['risk_score']}%")
    print(f"Reason  : {result['reason']}")

show_queue()
show_monitor()