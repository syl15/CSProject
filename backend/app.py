from flask import Flask, jsonify, request
import requests
import sys
from populate import raw_crisis_nlp_populate

# MAIN FLASK APP 
app = Flask(__name__)

@app.get("/")
def home():
    return "Hello, World!"

# FASTAPI APP 

FASTAPI_URL = "http://localhost:8000/predict"  # FastAPI endpoint

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

# MAIN APP 
if __name__ == "__main__":
    reset_db = "--reset-db" in sys.argv # optional argument to delete and repopulate raw_crisis_nlp_ table

    if reset_db:
        print("🔄 resetting and repopulating Raw_Crisis_NLP table...")
    else:
        print("Checking if Raw_Crisis_NLP table needs to be populated...")
        
    raw_crisis_nlp_populate(reset=reset_db)
