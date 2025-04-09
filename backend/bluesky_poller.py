from atproto import Client, client_utils
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from dateutil import parser
from database import get_db_connection
import os

'''
!!!!!!!!!
IMPORTANT NOTE:
For the purposes of testing, the sql commands in this file write to a TEMPORARY table called "temp_bluesky"
This temp table will be deleted after proper testing
Before deploying, ensure all sql commands are write to table "raw_bluesky"
!!!!!!!!!
'''

# create authenticated bsky session to access API
def authenticate_bsky():
    load_dotenv()

    USERNAME = os.getenv("BSKY_USERNAME")
    APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD")

    client = Client()
    client.login(USERNAME, APP_PASSWORD)
    return client

# create the raw bluesky table if it doesn't exist
def create_raw_bluesky_table():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            #TODO: change temp_bluesky to raw_bluesky
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS temp_bluesky (
                    Post_ID TEXT PRIMARY KEY,
                    Post_Original_Text TEXT,
                    Post_Time_Created_At TIMESTAMP,
                    Post_User_Handle TEXT,
                    Post_Link TEXT,
                    Post_Total_Interactions INTEGER,
                    Post_Keyword TEXT,
                    Model_Disaster_Label TEXT,
                    Model_Sentiment_Rating DECIMAL
                    Disaster_ID INT
                );
            ''')
            conn.commit()
            print("✅ raw_bluesky table is ready.")
        else:
            print("❌ Could not connect to database.")
    except Exception as e:
        print("Error creating table:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()  

# insert post data into the database
def insert_bluesky_data(batch_posts):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            #TODO: change temp_bluesky to raw_bluesky
            cursor.executemany('''
                INSERT INTO temp_bluesky (Post_ID, Post_Original_Text, Post_Time_Created_At, Post_User_Handle, Post_Link, Post_Total_Interactions, Post_Keyword, Model_Disaster_Label,
                    Model_Sentiment_Rating)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (Post_ID) DO NOTHING;
            ''', batch_posts)

            conn.commit()
            #TODO: change temp_bluesky to raw_bluesky
            print(f"✅ {len(batch_posts)} inserted into temp_bluesky.")
        else:
            print("❌ Could not connect to database.")
    except Exception as e:
        print("Error inserting data:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close() 

# search for certain # of posts given keyword
def poll_bsky_posts(client, keywords=["hurricane", "flood", "wildfire", "earthquake"], limit=25):
    time_limit = datetime.now(timezone.utc) - timedelta(hours=24)
    batch_posts = []

    for keyword in keywords:
        params = {"q": keyword, "limit": limit}
        posts = client.app.bsky.feed.search_posts(params)

        for post in posts.posts:
            # prevent pulling posts older than the past 24 hours to avoid duplicates
            post_time = parser.isoparse(post.record.created_at)
            if post_time > time_limit:
                #TODO: checking that URI, author, and handle are not null before accessing
                post_id = post.uri.split("/")[-1]
                post_original_text = post.record.text
                post_time_created_at = post.record.created_at
                post_user_handle = post.author.handle
                post_link = f"https://bsky.app/profile/{post.author.handle}/post/{post_id}"
                post_total_interactions = post.like_count + post.quote_count + post.reply_count + post.repost_count
                post_keyword = keyword
                model_label = None
                model_sentiment = None
    
                # add post data to the batch list
                batch_posts.append((post_id, post_original_text, post_time_created_at, post_user_handle, post_link, post_total_interactions, post_keyword, model_label, model_sentiment))

    if batch_posts:
        insert_bluesky_data(batch_posts)