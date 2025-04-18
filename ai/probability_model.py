import joblib
import os
from sklearn.ensemble import RandomForestClassifier

_model = None

def load_model():
    global _model
    if os.path.exists("model.pkl"):
        _model = joblib.load("model.pkl")
    else:
        _model = RandomForestClassifier()
        _model.fit([[0]*6], [0])  # modelo neutro para evitar falhas

load_model()

def predict_probability(features: dict) -> float:
    global _model
    X = [[
        features.get("price", 0),
        features.get("range", 0),
        features.get("distance_to_ote", 0),
        features.get("range", 0),
        features.get("range", 0),
        features.get("distance_to_ote", 0),
    ]]
    proba = _model.predict_proba(X)[0][1] if hasattr(_model, "predict_proba") else 0.5
    return round(float(proba), 2)
