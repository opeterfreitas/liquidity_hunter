import os
import xgboost as xgb
import numpy as np

class SignalClassifier:
    def __init__(self):
        self.model = None
        self.model_path = "models/saved/signal_model.xgb"

    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = xgb.XGBClassifier()
            self.model.load_model(self.model_path)
        else:
            raise FileNotFoundError(f"Modelo não encontrado em: {self.model_path}")

    def predict(self, features: dict) -> dict:
        if self.model is None:
            self.load_model()

        X = np.array([list(features.values())])
        proba = self.model.predict_proba(X)[0][1]
        prediction = int(proba > 0.5)

        return {
            "score": round(proba, 4),
            "predicted_label": prediction,
            "approved": prediction == 1
        }
