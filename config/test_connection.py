import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST_LOCALHOST"),  # <- use localhost aqui
    port=os.getenv("POSTGRES_PORT")
)

print("PostgreSQL connected:", conn.status)
conn.close()
