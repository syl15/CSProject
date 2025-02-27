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

# ----------------------------------------
# DATA LOADING AND FORMATTING 
# ----------------------------------------

def load_mock_data(): 
    """Loads mock disaster data from a  JSON file"""

    with open("mock_disaster_data.json", "r") as file: 
        return json.load(file) 
    
mock_disasters = load_mock_data()

# Format result to maintain attribute order 
def format_disaster(disaster): 
    """
    Formats a disaster entry as an OrderedDict to maintain original attribute order. 

    Args: 
        disaster(dict): A dictionary representing a disaster
    
    Returns: 
        OrderedDict: A disaster entry with consistent attribute ordering.
    """

    return OrderedDict([
            ("id",  disaster["id"]),
            ("name", disaster["name"]),
            ("startDate", disaster["startDate"]),
            ("endDate", disaster["endDate"]),
            ("totalTweets", disaster["totalTweets"]),
            ("severity", disaster["severity"]),
            ("summary", disaster["summary"]),
            ("location", disaster["location"]),
            ("locationName", disaster["locationName"]),
            ("sentiment", disaster["sentiment"]),
            ("topTweets", disaster["topTweets"]),
        ])

# ----------------------------------------
# DISASTER ENDPOINTS 
# ----------------------------------------

@app.get("/disasters")
def get_disasters(): 
    """
    Retrieves a list of disasters, optionally filtered by start and end date.

    Query Parameters:
        - limit (int, optional): The number of disasters to return. Default is 10.
        - startDate (str, optional): Filters disasters that started on or after this date (YYYY-MM-DD).
        - endDate (str, optional): Filters disasters that ended on or before this date (YYYY-MM-DD).

    Returns:
        JSON: A list of disasters matching the filters.
    """

    limit = int(request.args.get("limit", 10)) # Default=10 disasters 
    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")
    
    # Filter disasters by startDate and endDate if provided
    filtered_disasters = [ 
        disaster for disaster in mock_disasters
        if (not start_date or disaster["startDate"] >= start_date) and
            (not end_date or disaster["endDate"] <= end_date)
    ]

    formatted_disasters = [format_disaster(disaster) for disaster in filtered_disasters[:limit]]

    return app.response_class(
        json.dumps(formatted_disasters, indent=2), 
        mimetype="application/json"
    )


@app.get("/disasters/recent")
def get_recent_disaster(): 
    """
    Retrieves the most recent disaster based on start date.

    Returns:
        JSON: The most recent disaster.
    """
    recent_disaster = max(mock_disasters, key=lambda disaster: disaster["startDate"])

    return app.response_class(
        json.dumps(format_disaster(recent_disaster), indent=2), 
        mimetype="application/json"
    )


# ----------------------------------------
# MODEL PREDICTION ENDPOINT (FASTAPI)
# ----------------------------------------

FASTAPI_URL = "http://localhost:8000/predict"

@app.post("/predict")
def make_prediction(): 
    """
    Sends input text to the FastAPI model for prediction.

    Request Body:
        {
            "text": "Some input text"
        }

    Returns:
        JSON: The model's prediction.
    """
    data = request.get_json() 
    text = data.get("text")

    response = requests.post(FASTAPI_URL, json={"text": text})
    if response.status_code == 200:
        return jsonify(response.json())
    else: 
        return jsonify({"Error:" "Failed to get prediction"}), 500

@app.post("/mock-predict")
def mock_prediction(): 
    """
    Returns a mock response for testing the Flask API without calling FastAPI.

    Returns:
        JSON: A mock prediction result.
    """
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