from queue_manager import add_patient, show_queue
from monitor import show_monitor

patients = [
    {
        "age": 70,
        "symptoms": "chest pain",
        "heart_rate": 120,
        "blood_pressure": "90/60",
        "temperature": 37,
        "spo2": 85,
        "pain_score": 9
    },
    {
        "age": 30,
        "symptoms": "fever",
        "heart_rate": 105,
        "blood_pressure": "120/80",
        "temperature": 38.5,
        "spo2": 96,
        "pain_score": 5
    },
    {
        "age": 25,
        "symptoms": "headache",
        "heart_rate": 75,
        "blood_pressure": "120/80",
        "temperature": 36.8,
        "spo2": 98,
        "pain_score": 2
    }
]

def simple_triage(patient):
    if patient["spo2"] < 90 or "chest pain" in patient["symptoms"].lower():
        return "Critical"
    elif patient["heart_rate"] > 100 or patient["temperature"] > 38:
        return "Urgent"
    else:
        return "Normal"

for p in patients:
    severity = simple_triage(p)
    add_patient(p, severity)

show_queue()
show_monitor()