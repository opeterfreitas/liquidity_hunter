from db.repository import SessionLocal
from db.models import Signal
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_model():
    print("🤖 Treinando IA com sinais armazenados...")
    session = SessionLocal()
    signals = session.query(Signal).all()
    if not signals:
        print("⚠️ Nenhum dado para treinar.")
        return

    df = pd.DataFrame([s.__dict__ for s in signals])
    df = df.drop(columns=["_sa_instance_state", "created_at", "symbol", "direction", "confluences"])

    df["target"] = df["hit_tp"].astype(int)
    X = df[["entry", "tp", "sl", "ote_min", "ote_max", "confidence"]]
    y = df["target"]

    model = RandomForestClassifier()
    model.fit(X, y)
    joblib.dump(model, "model.pkl")

    print("✅ Modelo treinado e salvo.")
