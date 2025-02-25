import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)
database_url = os.getenv('DATABASE_URL') # Load DB environment variable
connection = psycopg2.connect(database_url) # Connect to the PostgreSQL database

@app.get("/")
def home():
    return "Hello, World!"