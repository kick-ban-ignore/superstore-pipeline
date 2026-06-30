# debug_env.py

# Test 1: .env-Datei roh einlesen
print("=== RAW .env INHALT ===")
with open(".env", "rb") as f:  # "rb" = raw bytes, kein Encoding-Parsing
    raw = f.read()
    print(raw)
    print()

# Test 2: dotenv laden und Werte prüfen  
from dotenv import load_dotenv
import os

load_dotenv()
print("=== GELADENE WERTE ===")
print(f"DB_HOST:     '{os.getenv('DB_HOST')}'")
print(f"DB_PORT:     '{os.getenv('DB_PORT')}'")
print(f"DB_NAME:     '{os.getenv('DB_NAME')}'")
print(f"DB_USER:     '{os.getenv('DB_USER')}'")
print(f"DB_PASSWORD: '{os.getenv('DB_PASSWORD')}'")