import os
import pandas as pd
from models.predictors.signal_classifier import SignalClassifier
from models.utils.feature_engineering import extract_features
from config.constants import MIN_TRAIN_SIZE
from glob import glob

def auto_retrain_from_logs():
    all_logs = []

    for file in glob("logs/*.jsonl"):
        with open(file, "r") as f:
            for line in f:
                try:
                    log = eval(line.strip())
                    if "label" in log and log["label"] in [1, 0, -1]:
                        all_logs.append(log)
                except:
                    continue

    if len(all_logs) < MIN_TRAIN_SIZE:
        print(f"[IA] 🔁 Retrain ignorado: apenas {len(all_logs)} exemplos válidos.")
        return

    print(f"[IA] 🧠 Iniciando retrain com {len(all_logs)} exemplos...")

    features = [extract_features(l) for l in all_logs]
    labels = [l["label"] for l in all_logs]

    df = pd.DataFrame(features)
    y = pd.Series(labels)

    clf = SignalClassifier()
    clf.retrain(df, y)

    print("[IA] ✅ Modelo reentrenado e salvo com sucesso.")
