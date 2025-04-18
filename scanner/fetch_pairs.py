import requests

def get_top_perpetuals(limit=400):
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        perpetuals = [
            s['symbol'] for s in data['symbols']
            if s.get('contractType') == 'PERPETUAL'
        ]

        print(f"🔧 Pares PERPETUAL obtidos: {len(perpetuals)}")
        return sorted(perpetuals)[:limit]

    except Exception as e:
        print(f"❌ Erro ao buscar pares da Binance: {e}")
        return []
