# utils/logger.py

from datetime import datetime

def log_rodada(tipo, analisados, gerados, ignorados, obs=None):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] 🧠 Resultado da rodada ({tipo}):")
    print(f"  - 🔍 Sinais analisados: {analisados}")
    print(f"  - ✅ Sinais gerados: {gerados}")
    print(f"  - ⚠️ Sinais ignorados: {ignorados}")
    if obs:
        print(f"  - 📝 Observação: {obs}")
