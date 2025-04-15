def extract_features(log: dict) -> dict:
    filters = log.get("filters", [])
    return {
        "rr": log.get("rr", 0),
        "has_ote": int("OTE" in filters),
        "has_ob": int("OB" in filters),
        "has_fvg": int("FVG" in filters),
        "has_sweep": int("Sweep" in filters),
        "has_choch": int("CHoCH" in filters),
        "has_mss": int("MSS" in filters),
        "confidence_score": log.get("confidence_score", 0),
    }
