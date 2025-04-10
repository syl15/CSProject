from flask import Flask, jsonify, request
from flask_cors import CORS 
import json
from collections import OrderedDict
from database import get_db_connection
from datetime import datetime
import sys 

# ----------------------------------------
# FLASK APP SETUP 
# ----------------------------------------
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"]) 

@app.get("/")
def home():
    return "Disaster Endpoints API"

# Health check to warm service
@app.get("/health")
def health():
    return "OK", 200

# ----------------------------------------
# DISASTER ENDPOINTS 
# ----------------------------------------

@app.get("/disasters")
def get_disasters(): 
    """
    Retrieves a summary list of disasters, optionally filtered by start and end date.

    Query Parameters:
        - limit (int, optional): The number of disasters to return. Default is 10.
        - startDate (str, optional): Filters disasters that started on or after this date (YYYY-MM-DD).

    Returns:
        JSON: A list of disasters matching the filters.
    """
    conn = get_db_connection() 
    cursor = conn.cursor()

    # Parse query parameters 
    limit_param = request.args.get("limit")
    limit = int(limit_param) if limit_param else None

    start_date = request.args.get("startDate")

    # Get all base disaster info 
    cursor.execute("""
            SELECT id, 
                   name, 
                   date, 
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

    disasters = [] 

    for row in disaster_rows: 
        disaster_id = row[0]
        event_type = event_type_map.get(disaster_id, "unknown")
        sentiment = sentiment_map.get(disaster_id)

        if sentiment: 
            overall = sentiment[4]
        else:
            overall = "unknown"

        disaster = OrderedDict([
            ("id", disaster_id),
            ("name", row[1]),
            ("eventType", event_type),
            ("startDate", row[2].isoformat()),
            ("locationName", row[3]),
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
        total = pos + neg + neu

        sentiment_dict  = {
            "positive": pos, 
            "negative": neg, 
            "neutral": neu
        }

        # Compute a severity score 
        # How many people are upset + how strongly they express it
        sentiment_balance = (neg - pos) / total if total else 0 
        hybrid_score = sentiment_balance + (-1 * median if median else 0) 

        if hybrid_score <= -1.0: # Strongly positive
            severity = 1
        elif hybrid_score <= -0.3:
            severity = 2
        elif hybrid_score <= 0.3:
            severity = 3
        elif hybrid_score <= 0.8: 
            severity = 4
        else:
            severity = 5 # Strongly negative

    else:
        sentiment_dict = {"positive": 0, "negative": 0, "neutral": 0}
        overall = "unknown"
        severity = 2 # Defaults to neutral

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

        else:
            sentiment_dict = {"positive": 0, "negative": 0, "neutral": 0}
            overall = "unknown"
            severity = 2 # Defaults to neutral

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

        # Get 5 posts
        cursor.execute("""
                SELECT 
                    poster_name, 
                    post_user_handle, 
                    post_original_text, 
                    post_time_created_at, 
                    post_link, 
                    model_sentiment_rating
                FROM temp_bluesky
                WHERE disaster_id = %s
                LIMIT 5     
        """, (disaster_id,))
        post_rows = cursor.fetchall()

        posts = [] 
        for r in post_rows:
            posts.append({
                "posterName": r[0] if r[0] else "Unknown",
                "username": r[1],
                "content": r[2],
                "timestamp": r[3].isoformat() if r[3] else None,
                "link": r[4],
                "sentimentScore": float(r[5]) if r[5] is not None else 0.0
            })

        # Build final disaster object (match format of /disasters)
        disaster = OrderedDict([
            ("id", row[0]),
            ("name", row[1]),
            ("totalPosts", total_posts),
            ("severity", severity),
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

    # Get top 10 posts
    cursor.execute("""
            SELECT 
                poster_name, 
                post_user_handle, 
                post_original_text, 
                post_time_created_at, 
                post_link, 
                model_sentiment_rating
            FROM temp_bluesky
            WHERE disaster_id = %s
            LIMIT 10     
    """, (disaster_id,))
    post_rows = cursor.fetchall()

    posts = [] 
    for r in post_rows:
        posts.append({
            "posterName": r[0] if r[0] else "Unknown",
            "username": r[1],
            "content": r[2],
            "timestamp": r[3].isoformat(),
            "link": r[4],
            "sentimentScore": float(r[5])
        })

    # Build final disaster object (match format of /disasters)
    disaster = OrderedDict([
        ("id", row[0]),
        ("name", row[1]),
        ("totalPosts", total_posts),
        ("severity", severity),
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

        sys.stdout.write(f"Returning disaster {disaster_id}\n")
        sys.stdout.flush()

        try:
            body = json.dumps(disaster, indent=2, ensure_ascii=False)
        except Exception as e:
            sys.stdout.write(f"json.dumps failed for disaster {disaster_id}: {e}\n")
            sys.stdout.flush()
            return jsonify({"error": f"Serialization failed for disaster {disaster_id}"}), 500

        return app.response_class(body, mimetype="application/json")
        
    except Exception as e: 
        sys.stdout.write(f"Error in /disasters/{disaster_id}: {e}\n")
        sys.stdout.flush()
        return jsonify({"error": f"Internal server error on disaster {disaster_id}"}), 500

@app.get("/disasters/recent")
def get_most_recent_disaster(): 
    """
    Retrieves the most recent disaster based on id.

    Returns:
        JSON: The most recent disaster with full metadata and top posts.
    """
    conn = get_db_connection() 
    cursor = conn.cursor() 

    # Get the ID of the most recent disaster 
    cursor.execute("""
            SELECT id
            FROM disaster_information
            ORDER BY id DESC
            LIMIT 1;
    """)

    row = cursor.fetchone() 
    if not row: 
        return jsonify({"erorr" : "No disasters found"}), 404
    
    most_recent_id = row[0]
    
    cursor.close() 
    conn.close() 

    # Forward to /disasters/<id> endpoint
    return get_disaster_by_id(most_recent_id)
