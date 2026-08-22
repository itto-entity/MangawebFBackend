import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine, text
from app.core.config import settings
load_dotenv()

url = settings.database_url
print("Connecting...")

try:
    conn = psycopg2.connect(url)
    print("DATABASE CONNECTED")
    conn.close()
except Exception as e:
    print("FAILED:")
    print(e)