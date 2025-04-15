import os
import json
from datetime import datetime
from config.settings import Settings

def log_signal_event(event_data: dict, asset: str, timeframe: str) -> None:
    """
    Salva o evento em formato .jsonl estruturado.
    """
    # Garantir diretório
    os.makedirs(Settings.LOGS_DIR, exist_ok=True)

    # Formatar nome do arquivo por data/ativo/timeframe
    today = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"{today}_{asset.lower()}_{timeframe.lower()}.jsonl"
    file_path = os.path.join(Settings.LOGS_DIR, filename)

    # Adicionar timestamp do evento
    event_data["timestamp"] = datetime.utcnow().isoformat()

    # Salvar como linha JSON
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event_data) + "\n")
