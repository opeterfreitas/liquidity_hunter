import requests
from config.settings import Settings

def send_signal_text(log: dict):
    direction = "📈 BUY" if log["tp"] > log["entry"] else "📉 SELL"
    text = f"""
🚨 *Sinal ICT Detected*
{direction} - {log['pair']} [{log['timeframe']}]

🎯 Entrada: `{log['entry']}`
🎯 TP: `{log['tp']}`
🛑 SL: `{log['sl']}`
⚖️ RR: `{log['rr']}`
🤖 Score IA: `{log['confidence_score']}`

📌 Confluências: {', '.join(log['filters'])}
🧠 IA: `{log['predicted_label']}` ({'✅ Aprovado' if log['approved'] else '❌ Rejeitado'})
🔁 Resultado: `{log['result']}`

*Sinal antecipado – Liquidity Hunter 🔍*
"""
    url = f"https://api.telegram.org/bot{Settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": Settings.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def send_signal_image(image_path: str):
    url = f"https://api.telegram.org/bot{Settings.TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as img:
        payload = {
            "chat_id": Settings.TELEGRAM_CHAT_ID,
        }
        files = {
            "photo": img
        }
        requests.post(url, data=payload, files=files)

def send_tp_notification(log: dict):
    direction = "📈 BUY" if log["tp"] > log["entry"] else "📉 SELL"
    message = f"""
✅ *TP Atingido!*  
{direction} - {log['pair']} [{log['timeframe']}]

🎯 Entrada: `{log['entry']}`  
🎯 TP: `{log['tp']}`  
🧠 Resultado confirmado: *TP*

*Liquidity Hunter em ação 🔥*
"""
    url = f"https://api.telegram.org/bot{Settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": Settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)
