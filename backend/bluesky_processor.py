'''
Could use postgresql notify/listen/trigger to alert the backend when new data has been added to the DB
However, this may cause issues with data being processed by the models if backend's connection to the DB goes idle and is disconnected b/c we are on a free plan
Since the poller is runs on a schedule, we can estimate when to make calls to FastAPI
As soon as bluesky_poller.py has run, we will immediately batch process all new data added to the DB
'''

import requests
import psycopg2
from database import get_db_connection
from config import get_deployed_fastapi_link, get_local_fastapi_link
from datetime import datetime

DEPLOYED_BASE_URL = get_deployed_fastapi_link()
LOCAL_BASE_URL = get_local_fastapi_link()

# swap out deployed constant with local constant and vice versa
CLASSIFICATION_API_URL = f"{DEPLOYED_BASE_URL}/predict-disaster"
SENTIMENT_API_URL = f"{DEPLOYED_BASE_URL}/predict-sentiment"

# batch fetch new bluesky posts
def fetch_unprocessed_posts():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Post_ID, Post_Original_Text FROM temp_bluesky
            WHERE Model_Disaster_Label IS NULL;
        """)

        # set consists of (Post_ID, Post_Original_Text)
        posts = cursor.fetchall()
        return posts

    except Exception as e:
        print("Error fetching unprocessed posts:", e)
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# batch request classification and sentiment models
def classify_posts(posts):
    classified_results = []
    for post_id, text in posts:
        response = requests.post(CLASSIFICATION_API_URL, json={"text": text})

        if response.status_code == 200:
            event_type = response.json()["event_type"]
            classified_results.append((post_id, event_type))
        else:
            print(f"❌ Classification failed for {post_id}")
            classified_results.append((post_id, "unrelated"))
            print(f"Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")

    return classified_results

# sentiment analysis if the disaster label is not unrelated
def analyze_sentiment(posts):
    sentiment_results = []
    for post_id, text, disaster_label in posts:
        if disaster_label == "unrelated":
            sentiment_results.append((post_id, None))
            continue

        response = requests.post(SENTIMENT_API_URL, json={"text": text})

        if response.status_code == 200:
            sentiment_score = response.json()["sentiment_score"]
            sentiment_results.append((post_id, sentiment_score))
        else:
            print(f"❌ Sentiment analysis failed for {post_id}")
            sentiment_results.append((post_id, None))

    return sentiment_results

# update DB with results from models
def update_database(classified_results, sentiment_results):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for post_id, disaster_label in classified_results:
            cursor.execute("""
                UPDATE temp_bluesky
                SET Model_Disaster_Label = %s
                WHERE Post_ID = %s;
            """, (disaster_label, post_id))

        for post_id, sentiment_score in sentiment_results:
            cursor.execute("""
                UPDATE temp_bluesky
                SET Model_Sentiment_Rating = %s
                WHERE Post_ID = %s;
            """, (sentiment_score, post_id))

        conn.commit()
        print(f"✅ Database updated with {len(classified_results)} classifications and {len(sentiment_results)} sentiment scores.")

    except Exception as e:
        print("Error updating database:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# drop all posts where disaster label is unrelated -- we no longer need to store these
def remove_unrelated_posts():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # fetch unrelated posts before deletion
        cursor.execute("""
            SELECT Post_ID, Post_Original_Text, Post_Time_Created_At, Post_User_Handle, Post_Link 
            FROM temp_bluesky
            WHERE Model_Disaster_Label = 'unrelated';
        """)
        unrelated_posts = cursor.fetchall()

        # log unrelated posts so we can check that they're actually "unrelated" to assess model performance
        with open("unrelated_posts.txt", "a") as log_file:
            log_file.write("\nPolled on " + str(datetime.now()) + "\n")
            log_file.write("\n=== Removed Unrelated Posts ===\n")
            for post in unrelated_posts:
                log_entry = (
                    f"Post ID: {post[0]}\n"
                    f"Text: {post[1]}\n"
                    f"Created At: {post[2]}\n"
                    f"User: {post[3]}\n"
                    f"Link: {post[4]}\n"
                    f"--------------------------\n"
                )
                log_file.write(log_entry)

        cursor.execute("""
            DELETE FROM temp_bluesky
            WHERE Model_Disaster_Label = 'unrelated';
        """)

        conn.commit()
        print(f"✅ {len(unrelated_posts)} unrelated posts removed from database.")

    except Exception as e:
        print("Error deleting unrelated posts:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 
def process_bluesky_data():
    print("🔄 Starting Bluesky data processing...")

    posts = fetch_unprocessed_posts()
    if not posts:
        print("🚫 No new posts to process.")
        return

    classified_results = classify_posts(posts)

    sentiment_inputs = [(pid, text, label) for (pid, text), label in zip(posts, [c[1] for c in classified_results])]
    sentiment_results = analyze_sentiment(sentiment_inputs)

    update_database(classified_results, sentiment_results)
    remove_unrelated_posts()

    print("✅ Processing completed!")