import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from triage_module.model_logic import predict_triage

# ===== DEMO CASES =====
cases = [
    {
        "name": "Case 1 - Critical",
        "age": 68,
        "heart_rate": 130,
        "spo2": 85,
        "temperature": 37.0,
        "pain_score": 9,
        "chest_pain": 1,
        "fever": 0,
        "headache": 0,
        "shortness_of_breath": 1
    },
    {
        "name": "Case 2 - Urgent",
        "age": 40,
        "heart_rate": 108,
        "spo2": 93,
        "temperature": 38.7,
        "pain_score": 6,
        "chest_pain": 0,
        "fever": 1,
        "headache": 0,
        "shortness_of_breath": 1
    },
    {
        "name": "Case 3 - Normal",
        "age": 25,
        "heart_rate": 74,
        "spo2": 98,
        "temperature": 36.8,
        "pain_score": 2,
        "chest_pain": 0,
        "fever": 0,
        "headache": 1,
        "shortness_of_breath": 0
    },
    {
        "name": "Case 4 - Critical (elderly)",
        "age": 82,
        "heart_rate": 135,
        "spo2": 83,
        "temperature": 37.3,
        "pain_score": 10,
        "chest_pain": 1,
        "fever": 0,
        "headache": 0,
        "shortness_of_breath": 1
    },
    {
        "name": "Case 5 - Urgent (fever + breathing)",
        "age": 35,
        "heart_rate": 109,
        "spo2": 92,
        "temperature": 39.1,
        "pain_score": 5,
        "chest_pain": 0,
        "fever": 1,
        "headache": 0,
        "shortness_of_breath": 1
    }
]

# ===== COLOR LABELS =====
COLORS = {
    "Critical": "🔴",
    "Urgent":   "🟡",
    "Normal":   "🟢"
}

# ===== RUN ALL CASES =====
if __name__ == "__main__":
    print("\n" + "="*50)
    print("   ED AI TRIAGE SYSTEM — TEST RESULTS")
    print("="*50)

    for case in cases:
        data = {k: v for k, v in case.items() if k != "name"}
        result = predict_triage(data)
        icon = COLORS.get(result["severity"], "⚪")

        print(f"\n📋 {case['name']}")
        print(f"   Severity   : {icon} {result['severity']}")
        print(f"   Risk Score : {result['risk_score']}%")
        print(f"   Reason     : {result['reason']}")
        print(f"   Method     : {result['method']}")
        print("-"*50)

    print("\n✅ All test cases completed.\n")