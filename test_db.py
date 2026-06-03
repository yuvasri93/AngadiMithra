import mysql.connector
import os
from dotenv import load_dotenv 
from pathlib import Path

# This forces Python to look in the exact same folder where this test_db.py file lives
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

print("HOST:", os.getenv("DB_HOST"))
print("USER:", os.getenv("DB_USER"))
print("PASSWORD:", os.getenv("DB_PASSWORD"))

db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),      # Added "localhost" backup fallback
    user=os.getenv("DB_USER", "root"),           # Added "root" backup fallback
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "angadimithra") # Added database backup fallback
)

cursor = db.cursor()
print("Database Connected Successfully!")