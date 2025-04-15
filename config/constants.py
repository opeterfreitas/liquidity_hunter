# Fibonacci levels (reutilizável em OTE, FVG, OB)
FIB_61_8 = 0.618
FIB_70_5 = 0.705
FIB_79 = 0.79

# OTE default configuration (tuple format: lower, upper)
OTE_DEFAULT_RANGE = (FIB_61_8, FIB_79)

# Swing settings
DEFAULT_MINIMUM_SWING_SIZE = 0.0020

# Labels for ML models
LABEL_SUCCESS = 1
LABEL_FAILURE = 0
LABEL_NEAR_MISS = -1

# Order Block detection
OB_BODY_RATIO_MIN = 0.30  # corpo da vela deve ser ao menos 30% da range

# FVG detection
FVG_MINIMUM_GAP_SIZE = 0.0005  # valor padrão para considerar um gap relevante

# Sweep detector
LOOKBACK_CANDLES_SWEEP = 10
SWEEP_TOLERANCE_PIPS = 0.0002

# Estrutura de mercado
LOOKBACK_SWINGS_STRUCTURE = 10
MIN_STRUCTURE_DISTANCE = 0.0002

# IA
MODEL_PATH = "models/weights/signal_model.pkl"
SCORE_THRESHOLD = 0.80
MINIMUM_TRAIN_SIZE = 100  # para habilitar re-treino

# IA
MIN_TRAIN_SIZE = 100
MODEL_PATH = "models/weights/signal_model.pkl"
RETRAIN_INTERVAL_HOURS = 24