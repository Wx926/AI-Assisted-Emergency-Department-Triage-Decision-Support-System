import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from model_logic import predict_triage

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    required = [
        "age", "heart_rate", "spo2", "temperature",
        "pain_score", "chest_pain", "fever",
        "headache", "shortness_of_breath"
    ]

    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    result = predict_triage(data)
    return jsonify(result), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Triage API is running"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)