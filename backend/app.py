from flask import Flask, jsonify, request
from flask_cors import CORS 
import requests
import sys
import json
from populate import raw_crisis_nlp_populate
from collections import OrderedDict
from database import get_db_connection
from datetime import datetime

# ----------------------------------------
# FLASK APP SETUP 
# ----------------------------------------
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"]) 

@app.get("/")
def home():
    return "Hello, World!"


# ----------------------------------------
# DISASTER ENDPOINTS 
# ----------------------------------------

# TODO: Remove any unnecessary fields in /disasters (only include those necessary for "All disasters" page)
@app.get("/disasters")
def get_disasters(): 
    """
    Retrieves a list of disasters, optionally filtered by start and end date.

    Query Parameters:
        - limit (int, optional): The number of disasters to return. Default is 10.
        - startDate (str, optional): Filters disasters that started on or after this date (YYYY-MM-DD).

    Returns:
        JSON: A list of disasters matching the filters.
    """
    conn = get_db_connection() 
    cursor = conn.cursor()

    # Parse query parameters 
    limit = int(request.args.get("limit", 10))
    start_date = request.args.get("startDate")

    # Get all base disaster info 
    cursor.execute("""
            SELECT id, 
                   name, 
                   date, 
                   summary, 
                   lat, 
                   long, 
                   radius, 
                   location_name
            FROM disaster_information; 
    """)

    disaster_rows = cursor.fetchall()
    
    # Filter by startDate if provided 
    if start_date: 
        try: 
            start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
            disaster_rows = [row for row in disaster_rows if row[2] >= start_dt]
        except ValueError: 
            return jsonify({"error": "Invalid startDate format. Use YYYY-MM-DD"}), 400

    # Fetch all sentiment metadata
    cursor.execute("""
            SELECT 
                disaster_id,
                COUNT(*) FILTER (WHERE model_sentiment_rating >= 0.05) AS positive,
                COUNT(*) FILTER (WHERE model_sentiment_rating <= -0.05) AS negative,
                COUNT(*) FILTER (
                    WHERE model_sentiment_rating > -0.05 AND model_sentiment_rating < 0.05
                ) AS neutral,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY model_sentiment_rating) AS median_score,
                CASE 
                    WHEN PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY model_sentiment_rating) >= 0.05 THEN 'positive'
                    WHEN PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY model_sentiment_rating) <= -0.05 THEN 'negative'
                    ELSE 'neutral'
                END AS overall_sentiment
            FROM temp_bluesky
            GROUP BY disaster_id
    """)
    
    sentiment_rows = cursor.fetchall() 
    sentiment_map = {row[0]: row[1:] for row in sentiment_rows}

    # Fetch event_type (most frequent disaster label per disaster, alphabetical tiebreaker)
    cursor.execute("""
            SELECT DISTINCT ON (disaster_id)
                disaster_id, 
                model_disaster_label AS event_type, 
                COUNT(*) AS count 
            FROM temp_bluesky 
            WHERE model_disaster_label is NOT NULL 
            GROUP BY disaster_id, model_disaster_label 
            ORDER BY disaster_id, COUNT(*) DESC, model_disaster_label ASC; 
    """)

    event_type_rows = cursor.fetchall() 
    event_type_map = {row[0]: row[1] for row in event_type_rows}

    # Fetch total post_count 
    cursor.execute("""
        SELECT disaster_id, COUNT(*) AS total_posts
        FROM temp_bluesky
        GROUP BY disaster_id;
    """)

    post_count_rows = cursor.fetchall()
    post_count_map = {row[0]: row[1] for row in post_count_rows}

    disasters = [] 

    for row in disaster_rows: 
        disaster_id = row[0]
        event_type = event_type_map.get(disaster_id, "unknown")
        total_posts = post_count_map.get(disaster_id, 0)
        sentiment = sentiment_map.get(disaster_id)

        if sentiment: 
            pos, neg, neu, median, overall = sentiment 
            sentiment_dict = {
                "positive": pos, 
                "negative": neg, 
                "neutral": neu
            }
        else:
            sentiment_dict = {"positive": 0, "negative": 0, "neutral": 0}
            overall = "unknown"

        disaster = OrderedDict([
            ("id", disaster_id),
            ("name", row[1]),
            ("totalPosts", total_posts), 
            ("eventType", event_type),
            ("startDate", row[2].isoformat()),
            ("summary", row[3]),
            ("location", {
                "latitude": float(row[4]),
                "longitude": float(row[5]),
                "radius": float(row[6])
            }), 
            ("locationName", row[7]),
            ("sentiment", sentiment_dict), 
            ("overallSentiment", overall)

        ])

        disasters.append(disaster)
    
    cursor.close() 
    conn.close() 

    return app.response_class(
        json.dumps(disasters[:limit], indent=2), 
        mimetype="application/json"
    )


@app.get("/disasters/<int:disaster_id>")
def get_disaster_by_id(disaster_id): 
    """
    Retrieves a single disaster by ID 

    Parameters: 
    - disaster_id (int): ID of the disaster to retrieve.

    Returns: 
        JSON: A single disaster object with metadata and top posts 
    """

    conn = get_db_connection() 
    cursor = conn.cursor() 

    # Get all base disaster info 
    cursor.execute("""
            SELECT id, 
                   name, 
                   date, 
                   summary, 
                   lat, 
                   long, 
                   radius, 
                   location_name
            FROM disaster_information
            WHERE id = %s;
    """, (disaster_id,))

    row = cursor.fetchone() 

    if not row: 
        return jsonify({"error": "Disaster not found"}), 404
    
    # Get sentiment
    cursor.execute("""
            SELECT 
                COUNT(*) FILTER (WHERE model_sentiment_rating >= 0.05),
                COUNT(*) FILTER (WHERE model_sentiment_rating <= -0.05),
                COUNT(*) FILTER (
                    WHERE model_sentiment_rating > -0.05 AND model_sentiment_rating < 0.05
                ),
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY model_sentiment_rating),
                CASE 
                    WHEN PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY model_sentiment_rating) >= 0.05 THEN 'positive'
                    WHEN PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY model_sentiment_rating) <= -0.05 THEN 'negative'
                    ELSE 'neutral'
                END
            FROM temp_bluesky
            WHERE disaster_id = %s
    """, (disaster_id,))

    sentiment = cursor.fetchone()
    if sentiment:
        pos, neg, neu, median, overall = sentiment
        sentiment_dict  = {
            "positive": pos, 
            "negative": neg, 
            "neutral": neu
        }
    else:
        sentiment_dict = {"positive": 0, "negative": 0, "neutral": 0}
        overall = "unknown"

     # Get event type
    cursor.execute("""
            SELECT model_disaster_label
            FROM temp_bluesky
            WHERE disaster_id = %s AND model_disaster_label IS NOT NULL
            GROUP BY model_disaster_label
            ORDER BY COUNT(*) DESC, model_disaster_label ASC
            LIMIT 1
    """, (disaster_id,))
    
    event_type_row = cursor.fetchone()
    event_type = event_type_row[0] if event_type_row else "unknown"

    # Get total post count
    cursor.execute("""
            SELECT COUNT(*) FROM temp_bluesky WHERE disaster_id = %s
    """, (disaster_id,))

    post_count = cursor.fetchone()
    total_posts = post_count[0] if post_count else 0

    # Get top 10 posts
    cursor.execute("""
            SELECT post_user_handle, post_original_text, post_time_created_at, post_link, model_sentiment_rating
            FROM temp_bluesky
            WHERE disaster_id = %s
            LIMIT 10     
    """, (disaster_id,))
    post_rows = cursor.fetchall()

    posts = [] 
    for r in post_rows:
        posts.append({
            "username": r[0],
            "content": r[1],
            "timestamp": r[2].isoformat(),
            "sentimentScore": float(r[4]),
            "link": r[3]
        })

    # Build final disaster object (match format of /disasters)
    disaster = OrderedDict([
        ("id", row[0]),
        ("name", row[1]),
        ("totalPosts", total_posts),
        ("eventType", event_type),
        ("startDate", row[2].isoformat()),
        ("summary", row[3]),
        ("location", {
            "latitude": float(row[4]),
            "longitude": float(row[5]),
            "radius": float(row[6])
        }),
        ("locationName", row[7]),
        ("sentiment", sentiment_dict), 
        ("overallSentiment", overall),
        ("posts", posts)
    ])

    cursor.close() 
    conn.close()

    return app.response_class(
        json.dumps(disaster, indent=2, ensure_ascii=False),
        mimetype="application/json"
    )

# ----------------------------------------
# MODEL PREDICTION ENDPOINT (FASTAPI)
# ----------------------------------------

# TODO: Eventually, make this an env variable, and add it to render.yaml under envVars
# FASTAPI_LIVE_URL = "https://fastapi-model-3vkm.onrender.com/predict-disaster"
FASTAPI_LOCAL_URL = "http://127.0.0.1:8000/predict-disaster"

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

    response = requests.post(FASTAPI_LOCAL_URL, json={"text": text})
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


# ----------------------------------------
# APPLICATION STARTUP 
# ----------------------------------------
 
if __name__ == "__main__":
    """
    Starts the Flask application.
    Optionally resets the database if '--reset-db' is passed as a command-line argument. (Not recommended)
    """
    reset_db = "--reset-db" in sys.argv # 

    if reset_db:
        print("🔄 resetting and repopulating Raw_Crisis_NLP table...")
    else:
        print("Checking if Raw_Crisis_NLP table needs to be populated...")
        
    raw_crisis_nlp_populate(reset=reset_db)
