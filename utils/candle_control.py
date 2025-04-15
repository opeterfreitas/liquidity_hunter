import os
import json
from datetime import datetime
from pathlib import Path

STATE_FILE = Path("state/last_candle_state.json")
os.makedirs(STATE_FILE.parent, exist_ok=True)

# Carrega estado do arquivo
def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

# Salva estado no arquivo
def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

# Retorna se o candle é novo para aquele par/timeframe
def candle_is_new(pair: str, timeframe: str, latest_candle_time: str) -> bool:
    """
    Verifica se é um candle novo. latest_candle_time deve estar em formato ISO (ex: 2025-04-14T15:00:00Z)
    """
    state = load_state()
    key = f"{pair}_{timeframe}"
    prev = state.get(key)

    if prev != latest_candle_time:
        state[key] = latest_candle_time
        save_state(state)
        return True
    return False
