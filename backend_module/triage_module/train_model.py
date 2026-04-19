import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv("triage_module/dataset.csv")

# Features and label
X = df.drop("severity", axis=1)
y = df["severity"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
print("=== MODEL EVALUATION ===")
print(classification_report(y_test, model.predict(X_test)))

# Save model
joblib.dump(model, "triage_module/triage_model.pkl")
print("Model saved to triage_module/triage_model.pkl")