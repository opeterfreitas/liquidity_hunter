import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )
    print("✅ Conexão com PostgreSQL bem-sucedida!")
    conn.close()
except Exception as e:
    print("❌ Erro ao conectar no banco:")
    print(e)
