import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    database_url = os.getenv('DATABASE_URL')
    return psycopg2.connect(database_url)