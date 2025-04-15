import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.pair_manager import get_active_pairs
from utils.candle_control import candle_is_new
from utils.binance_provider import get_latest_candle_time
from data.data_loader import load_price_data
from detectors.ote_zone_detector import detect_ote_zones
from detectors.order_block_detector import detect_order_blocks
from detectors.fair_value_gap_detector import detect_fvg_zones
from detectors.liquidity_sweep_detector import detect_liquidity_sweeps
from detectors.structure_shift_detector import detect_structure_breaks
from models.predictors.signal_classifier import SignalClassifier
from models.utils.feature_engineering import extract_features
from utils.structured_logger import log_signal_event
from visuals.signal_plotter import plot_signals
from telegram.sender import send_signal_text, send_signal_image
from models.trainers.auto_retrainer import auto_retrain_from_logs
from models.postprocessors.label_updater import update_labels_from_price_data
from models.metrics.performance_tracker import print_summary_after_round

TIMEFRAMES = ["D1", "H4", "H1", "M15", "M5"]

def run_signal_pipeline_for_pair_timeframe(pair: str, timeframe: str):
    try:
        logging.info(f"🔍 Analisando [{pair} | {timeframe}]...")

        df = load_price_data(pair, timeframe)

        ote_zones = detect_ote_zones(df)
        ob_zones = detect_order_blocks(df)
        fvg_zones = detect_fvg_zones(df)
        sweeps = detect_liquidity_sweeps(df)
        structure_breaks = detect_structure_breaks(df)

        confluences = []
        if ote_zones: confluences.append("OTE")
        if ob_zones: confluences.append("OB")
        if fvg_zones: confluences.append("FVG")
        if sweeps: confluences.append("Sweep")
        if any(sb.break_type == "choch" for sb in structure_breaks): confluences.append("CHoCH")
        if any(sb.break_type == "mss" for sb in structure_breaks): confluences.append("MSS")

        entry = df.iloc[-1]["close"]
        sl = entry - 0.0010
        tp = entry + 0.0020
        rr = round((tp - entry) / (entry - sl), 2)

        if rr < 2.0 or len(confluences) < 3:
            signal_log = {
                "pair": pair,
                "timeframe": timeframe,
                "entry": round(entry, 5),
                "tp": round(tp, 5),
                "sl": round(sl, 5),
                "rr": rr,
                "filters": confluences,
                "filtered_out": True,
                "label": -1,
                "result": "filtered"
            }
            log_signal_event(signal_log, asset=pair, timeframe=timeframe)
            logging.info(f"❌ Sinal descartado por qualidade (RR: {rr} | {len(confluences)} confluências)")
            return

        signal_log = {
            "pair": pair,
            "timeframe": timeframe,
            "entry": round(entry, 5),
            "tp": round(tp, 5),
            "sl": round(sl, 5),
            "rr": rr,
            "filters": confluences,
            "ote_zone": ote_zones[-1].to_dict() if ote_zones else None,
            "order_block": ob_zones[-1].to_dict() if ob_zones else None,
            "fvg": fvg_zones[-1].to_dict() if fvg_zones else None,
            "sweep": sweeps[-1].to_dict() if sweeps else None,
            "structure_break": structure_breaks[-1].to_dict() if structure_breaks else None,
        }

        logging.info(f"✅ Qualificado (RR: {rr} | Confluências: {', '.join(confluences)})")

        features = extract_features(signal_log)
        clf = SignalClassifier()
        decision = clf.predict(features)

        signal_log.update({
            "confidence_score": decision["score"],
            "predicted_label": decision["predicted_label"],
            "approved": decision["approved"],
        })

        if decision["approved"]:
            signal_log["label"] = 1
            signal_log["result"] = "pending"
            img_path = plot_signals(
                price_data=df,
                ote_zones=ote_zones,
                ob_zones=ob_zones,
                fvg_zones=fvg_zones,
                sweeps=sweeps,
                structure_breaks=structure_breaks,
                filename=f"{pair}_{timeframe}"
            )
            signal_log["image_path"] = img_path
            send_signal_image(img_path)
            send_signal_text(signal_log)
            logging.info(f"🤖 IA Score: {decision['score']} → Aprovado")
            logging.info("📤 Enviado para Telegram")
        else:
            signal_log["label"] = -1
            signal_log["result"] = "discarded"
            logging.info(f"⚠️ Sinal rejeitado pela IA (Score: {decision['score']})")

        log_signal_event(signal_log, asset=pair, timeframe=timeframe)

    except Exception as e:
        logging.error(f"❌ Erro no pipeline para {pair} {timeframe}: {str(e)}")

def run_all_pairs_all_timeframes():
    pairs = get_active_pairs()
    total_assets = len(pairs)
    total_timeframes = len(TIMEFRAMES)
    total_combinations = total_assets * total_timeframes
    execuções_realizadas = 0

    for pair in pairs:
        for tf in TIMEFRAMES:
            try:
                candle_time = get_latest_candle_time(pair, tf)
                if candle_is_new(pair, tf, candle_time):
                    run_signal_pipeline_for_pair_timeframe(pair, tf)
                    execuções_realizadas += 1
                else:
                    logging.info(f"🕒 [{pair} | {tf}] sem candle novo.")
            except Exception as e:
                logging.error(f"⚠️ Erro ao processar {pair} {tf}: {str(e)}")

    logging.info(f"📌 Execuções realizadas nesta rodada: {execuções_realizadas}")
    print_summary_after_round(
        total_assets=total_assets,
        total_timeframes=total_timeframes,
        total_combinations=total_combinations
    )

def start_scheduler():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    scheduler = BackgroundScheduler()

    scheduler.add_job(run_all_pairs_all_timeframes, "interval", minutes=10)
    scheduler.add_job(auto_retrain_from_logs, "interval", hours=24)
    scheduler.add_job(update_labels_from_price_data, "interval", hours=1)

    scheduler.start()
    logging.info("🚀 Liquidity Hunter rodando com scheduler ativo.")

    # 👇 Executa imediatamente a primeira rodada
    run_all_pairs_all_timeframes()

    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info("🛑 Scheduler encerrado.")

if __name__ == "__main__":
    start_scheduler()
