import os
import json
import glob
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from config.settings import Settings

# Caminho para os arquivos de log
LOG_DIR = "logs/"
OUTPUT_PATH = os.path.join(Settings.MODELS_DIR, "saved/signal_model.xgb")
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Todas as possíveis confluências (para one-hot encoding)
ALL_CONFLUENCES = ["OTE", "OB", "FVG", "Sweep", "CHoCH"]


def extract_features_and_labels():
    X, y = [], []
    files = glob.glob(os.path.join(LOG_DIR, "*.jsonl"))

    for file in files:
        with open(file, "r") as f:
            for line in f:
                try:
                    row = json.loads(line)
                    # Ignora sinais sem resultado (pendentes)
                    if row.get("result") not in [0, 1]:
                        continue
                    features = {
                        "rr": row.get("rr", 1.0),
                        **{f"conf_{c}": int(c in row.get("confluences", [])) for c in ALL_CONFLUENCES}
                    }
                    X.append(list(features.values()))
                    y.append(row["result"])
                except Exception as e:
                    print(f"❌ Erro no arquivo {file}: {e}")
    return X, y


def train_and_save_model():
    X, y = extract_features_and_labels()
    if not X:
        print("⚠️ Nenhum dado de treino encontrado. Treinamento abortado.")
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print("\n📊 Avaliação do Modelo:\n")
    print(classification_report(y_test, preds))

    joblib.dump(model, OUTPUT_PATH)
    print(f"\n✅ Modelo salvo com sucesso em: {OUTPUT_PATH}")


if __name__ == "__main__":
    train_and_save_model()
