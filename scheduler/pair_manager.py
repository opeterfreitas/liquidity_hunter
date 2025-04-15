import os
import json
import requests
from config.settings import Settings

PAIRS_CACHE_FILE = "scheduler/active_pairs.json"

def fetch_top_pairs_from_binance():
    """
    Busca os principais pares por volume da Binance
    """
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()

    usdt_pairs = [
        d for d in data
        if d["symbol"].endswith("USDT") and not d["symbol"].endswith("BUSD")
    ]

    sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x["quoteVolume"]), reverse=True)
    top_pairs = [p["symbol"] for p in sorted_pairs[:Settings.PAIRS_LIMIT]]

    return top_pairs

def get_active_pairs():
    """
    Retorna a lista de pares ativos, garantindo existência do arquivo e diretório
    """
    os.makedirs(os.path.dirname(PAIRS_CACHE_FILE), exist_ok=True)

    if not os.path.exists(PAIRS_CACHE_FILE):
        with open(PAIRS_CACHE_FILE, "w") as f:
            json.dump([], f)

    with open(PAIRS_CACHE_FILE, "r") as f:
        try:
            pairs = json.load(f)
        except json.JSONDecodeError:
            pairs = []

    if not pairs:
        try:
            pairs = fetch_top_pairs_from_binance()
            with open(PAIRS_CACHE_FILE, "w") as f:
                json.dump(pairs, f)
        except Exception as e:
            print(f"[⚠️] Erro ao buscar pares da Binance: {e}")
            pairs = []

    return pairs
