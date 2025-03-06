from flask import Flask, jsonify, request
from flask_cors import CORS 
import requests
import sys
from flask import Flask
import json
from populate import raw_crisis_nlp_populate
from collections import OrderedDict

# ----------------------------------------
# FLASK APP SETUP 
# ----------------------------------------
app = Flask(__name__)

#  TODO: Address connection problem later
# database_url = os.getenv('DATABASE_URL') # Load DB environment variable
# connection = psycopg2.connect(database_url) # Connect to the PostgreSQL database


FASTAPI_URL = "http://localhost:8000/predict"  # FastAPI endpoint
import sys
from flask import Flask
from populate import raw_crisis_nlp_populate

app = Flask(__name__)

@app.get("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    reset_db = "--reset-db" in sys.argv # optional argument to delete and repopulate raw_crisis_nlp_ table

    if reset_db:
        print("🔄 resetting and repopulating Raw_Crisis_NLP table...")
    else:
        print("Checking if Raw_Crisis_NLP table needs to be populated...")
        
    raw_crisis_nlp_populate(reset=reset_db)