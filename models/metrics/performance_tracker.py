import os
import json
import logging
from glob import glob

def print_summary_after_round(
    total_assets: int,
    total_timeframes: int,
    total_combinations: int
):
    tp = 0
    sl = 0
    approved = 0
    filtered = 0
    discarded = 0

    for file in glob("logs/*.jsonl"):
        with open(file, "r") as f:
            for line in f:
                try:
                    log = json.loads(line.strip())
                    result = log.get("result", "")
                    label = log.get("label", -1)

                    if result == "TP":
                        tp += 1
                    elif result == "SL":
                        sl += 1
                    elif result == "filtered":
                        filtered += 1
                    elif result == "discarded":
                        discarded += 1

                    if label == 1 and result == "pending":
                        approved += 1

                except:
                    continue

    total = tp + sl
    winrate = round(tp / total * 100, 2) if total > 0 else 0.0

    logging.info("\n" + "=" * 65)
    logging.info("📊 RESUMO DA RODADA")
    logging.info(f"📈 Ativos analisados             : {total_assets}")
    logging.info(f"⏱️  Timeframes por ativo         : {total_timeframes}")
    logging.info(f"🔁 Combinações processadas       : {total_combinations}")
    logging.info(f"✔️  Sinais aprovados pendentes   : {approved}")
    logging.info(f"🎯  TP confirmados               : {tp}")
    logging.info(f"🛑  SL confirmados               : {sl}")
    logging.info(f"❌  Filtrados por qualidade      : {filtered}")
    logging.info(f"🚫  Rejeitados pela IA           : {discarded}")
    logging.info(f"⚖️  Assertividade (TP / SL)      : {winrate}%")
    logging.info("=" * 65 + "\n")
