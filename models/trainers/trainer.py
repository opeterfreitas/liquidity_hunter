import pandas as pd
from models.predictors.signal_classifier import SignalClassifier
from models.utils.feature_engineering import extract_features

def train_from_jsonl(jsonl_path: str):
    logs = []
    with open(jsonl_path, "r") as f:
        for line in f:
            try:
                logs.append(eval(line.strip()))
            except:
                continue

    features = [extract_features(log) for log in logs]
    labels = [log.get("label", -1) for log in logs]

    df = pd.DataFrame(features)
    y = pd.Series(labels)

    # Apenas se houver volume suficiente
    if len(df) < 100:
        print(f"[IA] Dados insuficientes para treino ({len(df)} amostras)")
        return

    clf = SignalClassifier()
    clf.retrain(df, y)
    print(f"[IA] Modelo reentrenado com {len(df)} amostras.")
