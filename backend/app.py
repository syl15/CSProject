import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import requests

load_dotenv()

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


# Get prediction from our model 
@app.post("/predict")
def make_prediction(): 
    # Get text input from request 
    data = request.get_json() 
    text = data.get("text")

    response = requests.post(FASTAPI_URL, json={"text": text})
    if response.status_code == 200:
        return jsonify(response.json())
    else: 
        return jsonify({"Error:" "Failed to get prediction"}), 500

# Mock route to test Flask service 
@app.post("/mock-predict")
def mock_prediction(): 
    # Return mock response without calling FastAPI 
    return jsonify({"event_type": "Testing Flask"})

if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=5001) # Note: I used 5001 because 5000 was occupied on my port (by Airplay); we can change this if necessary
if __name__ == "__main__":
    reset_db = "--reset-db" in sys.argv # optional argument to delete and repopulate raw_crisis_nlp_ table

    if reset_db:
        print("🔄 resetting and repopulating Raw_Crisis_NLP table...")
    else:
        print("Checking if Raw_Crisis_NLP table needs to be populated...")
        
    raw_crisis_nlp_populate(reset=reset_db)
