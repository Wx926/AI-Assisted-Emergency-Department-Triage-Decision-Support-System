# TriagePulse — AI-Assisted Emergency Department Triage Decision Support System

> **Smarter Decisions. Faster Emergency Care.**

TriagePulse is an AI-powered triage decision support system built for Malaysia's Emergency Departments. It helps triage nurses prioritize patients faster, more consistently, and more safely using machine learning and Google Gemini AI.

---

## 🏥 Problem Statement

Malaysia's Emergency Departments face increasing patient volumes, limited staff capacity, and prolonged waiting times. MOH operational documents identify prolonged bed waiting time as a key contributor to ED overcrowding. Manual triage depends heavily on clinical judgment, which can vary under workload pressure.

**TriagePulse solves this by providing AI-assisted triage that is fast, consistent, and explainable.**

---

## 🤖 Solution Overview

TriagePulse is a web-based clinical decision support system that:

- Accepts patient vitals from the triage nurse
- Predicts severity level using a hybrid AI model (rule-based + Random Forest ML)
- Generates a clinical summary using **Google Gemini AI**
- Sorts the patient queue automatically by severity
- Fires critical alerts for high-risk patients
- Provides an admin dashboard for ED supervisors

---

## 🌟 Key Features

| Feature | Description |
|---|---|
| AI Triage Prediction | Hybrid rule-based + Random Forest ML model |
| Gemini Clinical Summary | Google Gemini AI generates doctor-ready summaries |
| Real-time Queue | Auto-sorted by severity — Critical first |
| Critical Alerts | Automatic alerts for high-risk patients |
| Discharge Management | Nurses can discharge patients directly from queue |
| Admin Dashboard | Real-time stats, charts, alerts, patient history |
| Multi-page UI | Separate pages for Home, Intake, Queue, Admin |
| Live ED Clock | Real-time system time display |

---

## 🛠️ Tech Stack

### AI & Backend
- **Python** — Core language
- **FastAPI** — REST API framework
- **Random Forest** (scikit-learn) — ML triage model
- **Google Gemini AI** (`gemini-2.0-flash`) — Clinical summary generation
- **SQLite** — Patient database

### Frontend
- **HTML5 / CSS3 / JavaScript** — Multi-page UI
- **Vanilla JS Fetch API** — Backend communication

### Google AI Ecosystem
- **Gemini API** — Clinical summary generation
- **Google Cloud Run** — Backend deployment
- **Google Cloud Build** — Container build pipeline
- **Artifact Registry** — Docker image storage

---

## 🏗️ System Architecture

```
UI (HTML/CSS/JS)
    ↓ HTTP POST
FastAPI Backend (Cloud Run)
    ↓
Rule-Based Safety Check
    ↓
Random Forest ML Model
    ↓
Google Gemini AI Summary
    ↓
SQLite Database
    ↓
Queue + Alerts
```

---

## 📁 Project Structure

```
AI-Assisted-Emergency-Department-Triage-Decision-Support-System/
│
├── backend_module/
│   ├── app.py              ← FastAPI app entry point
│   ├── routes.py           ← API routes + Gemini integration
│   ├── database.py         ← SQLite database setup
│   ├── Dockerfile          ← Cloud Run deployment
│   ├── .dockerignore
│   └── triage_module/      ← AI model (copied for deployment)
│
├── triage_module/
│   ├── model_logic.py      ← Prediction logic (rules + ML)
│   ├── train_model.py      ← Model training script
│   ├── triage_model.pkl    ← Trained Random Forest model
│   ├── dataset.csv         ← Training dataset (100 records)
│   └── test_cases.py       ← Demo test cases
│
├── integration_module/
│   ├── integration_test.py ← End-to-end integration test
│   ├── monitor.py          ← ED monitoring dashboard
│   └── queue_manager.py    ← Queue management logic
│
└── UI/
    ├── index.html          ← Home page
    ├── intake.html         ← Patient intake form
    ├── queue.html          ← Patient queue
    ├── admin.html          ← Admin dashboard
    └── index.css           ← Stylesheet
```

---

## 🚀 Live Deployment

| Service | URL |
|---|---|
| **Backend API (Cloud Run)** | https://triagepulse-backend-472704188167.asia-southeast1.run.app |
| **API Health Check** | https://triagepulse-backend-472704188167.asia-southeast1.run.app/ |
| **API Documentation** | https://triagepulse-backend-472704188167.asia-southeast1.run.app/docs |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/patients` | Add new patient |
| POST | `/triage/{patient_id}` | Run AI triage + Gemini summary |
| GET | `/queue` | Get sorted patient queue |
| GET | `/alerts` | Get active critical alerts |
| POST | `/discharge/{queue_id}` | Discharge patient from queue |

---

## ⚙️ How to Run Locally

### Prerequisites
- Python 3.11+
- pip

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/Wx926/AI-Assisted-Emergency-Department-Triage-Decision-Support-System.git
cd AI-Assisted-Emergency-Department-Triage-Decision-Support-System

# Install dependencies
pip install fastapi uvicorn google-generativeai scikit-learn pandas numpy joblib

# Copy triage module
xcopy triage_module backend_module\triage_module /E /I /Y

# Run backend
cd backend_module
uvicorn app:app --reload
```

### Frontend Setup

```bash
# In a new terminal
cd UI
python -m http.server 3000
```

Open browser: `http://127.0.0.1:3000`

---

## 🧪 Test the AI Model

```bash
cd triage_module
python test_cases.py
```

Expected output:
```
===== ED AI TRIAGE SYSTEM — TEST RESULTS =====

📋 Case 1 - Critical
   Severity   : 🔴 Critical
   Risk Score : 95%
   Reason     : RULE TRIGGERED: SpO2 below 90% or chest pain with high heart rate.

📋 Case 2 - Urgent
   Severity   : 🟡 Urgent
   Risk Score : 65%
   Reason     : Elevated heart rate and/or fever with moderate risk indicators.

📋 Case 3 - Normal
   Severity   : 🟢 Normal
   Risk Score : 20%
   Reason     : Vitals within acceptable range. No severe symptoms detected.
```

---

## 🎯 Triage Classification

| Severity | Criteria | Risk Score |
|---|---|---|
| 🔴 Critical | SpO2 < 90% OR chest pain + high HR | 90-95% |
| 🟡 Urgent | HR > 100 OR fever with moderate symptoms | 60-70% |
| 🟢 Normal | Stable vitals, no severe symptoms | 20% |

---

## 🤖 Gemini AI Integration

TriagePulse uses **Google Gemini AI** (`gemini-2.0-flash`) to generate clinical summaries for each triaged patient. After the ML model predicts severity, Gemini generates a professional 2-sentence clinical summary for the attending doctor.

Example output:
```
Patient Ahmad Razali, 68, presents with chest pain and critically low 
oxygen saturation of 85%. Immediate physician review is strongly 
recommended given the high-risk vital signs and elevated heart rate.
```

---

## 🌍 SDG Alignment

| SDG | Alignment |
|---|---|
| **SDG 3: Good Health and Well-Being** | Improves emergency healthcare delivery and patient safety |
| **SDG 9: Industry, Innovation and Infrastructure** | Applies AI to modernize hospital triage infrastructure |

---

## ⚠️ Ethics & Safety

- AI is **decision support only** — final triage decision remains with the clinician
- All recommendations are **explainable** with clear reasons
- System is designed to **minimize under-triage** of critical patients
- Patient data is handled with appropriate care

---

## Production Considerations
- Database: SQLite used for prototype. Cloud SQL (PostgreSQL) recommended for production deployment to ensure data persistence across Cloud Run restarts.
- Gemini API: Integrated via google-generativeai library. Vertex AI recommended for production deployment for better scalability and quota management.

## 📄 License

This project was built for the MyAI Future Hackathon 2026. For educational and demonstration purposes only.

---

*TriagePulse — Smarter Decisions. Faster Emergency Care.*
