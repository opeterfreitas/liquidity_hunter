import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    # Database
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)

    # Paths
    LOGS_DIR = os.getenv("LOGS_DIR", "./logs")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")

    # OTE
    MINIMUM_SWING_SIZE = float(os.getenv("MINIMUM_SWING_SIZE", 0.0020))

    # Configurações principais
    PAIRS_LIMIT = int(os.getenv("PAIRS_LIMIT", 20))

    # Caminho padrão para salvar o modelo treinado
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    MODELS_DIR = os.path.join(BASE_DIR, "models")