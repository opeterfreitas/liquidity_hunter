import os
import json
from glob import glob
import pandas as pd
from data.data_loader import load_price_data
from telegram.sender import send_tp_notification

def update_labels_from_price_data():
    logs_dir = "logs"
    updated = 0

    for file_path in glob(f"{logs_dir}/*.jsonl"):
        lines = []

        with open(file_path, "r") as f:
            for line in f:
                try:
                    log = json.loads(line.strip())

                    # Só processa sinais aprovados e ainda pendentes
                    if log.get("label") == 1 and log.get("result") == "pending":
                        pair = log["pair"]
                        tf = log["timeframe"]
                        entry = log["entry"]
                        tp = log["tp"]
                        sl = log["sl"]

                        # Carrega candles recentes para avaliar se TP ou SL foi atingido
                        df = load_price_data(pair, tf, limit=50)

                        outcome = "pending"
                        for i in range(len(df)):
                            low = df.iloc[i]["low"]
                            high = df.iloc[i]["high"]

                            if low <= sl:
                                outcome = "SL"
                                label = 0
                                break
                            elif high >= tp:
                                outcome = "TP"
                                label = 1
                                break

                        # Atualiza log se necessário
                        if outcome != "pending":
                            log["result"] = outcome
                            log["label"] = label
                            log["label_updated"] = True
                            updated += 1

                            # Envia mensagem para Telegram se atingiu TP
                            if outcome == "TP":
                                send_tp_notification(log)

                    # Salva linha atualizada ou inalterada
                    lines.append(json.dumps(log))

                except Exception as e:
                    print(f"[LOG ERROR] {file_path}: erro ao processar linha -> {e}")

        # Reescreve o arquivo com logs atualizados
        with open(file_path, "w") as f:
            f.write("\n".join(lines) + "\n")

    print(f"[LOG CHECK] ✅ {updated} sinais atualizados com TP ou SL.")
