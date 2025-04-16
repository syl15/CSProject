#------------------------------------------------------------------------
# DATABASE QUERYING FUNCTIONS FOR CLUSTERING
#------------------------------------------------------------------------
from database import get_db_connection
import psycopg2
import numpy as np

def create_disaster_table():
    try:
        print("Creating disaster table...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS disaster_information (
                id SERIAL PRIMARY KEY,
                name TEXT,
                location_name TEXT, 
                centroid FLOAT8[],
                lat DOUBLE PRECISION,
                long DOUBLE PRECISION,
                radius DOUBLE PRECISION,
                date DATE,
                event_type TEXT,
                overall_sentiment TEXT,
                summary TEXT
            );
        """)
        conn.commit()
        print("Disaster table created successfully.")
    
    except Exception as e:
        print("Error creating disaster table:", e)
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# load existing disaster centroids
def load_existing_disasters():
    try:
        print("Loading existing disasters...")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, centroid 
            FROM disaster_information;
        """)
        
        results = cursor.fetchall()
        disasters = [(disaster_id, np.array(centroid)) for disaster_id, centroid in results]
        
        print(f"Loaded {len(disasters)} existing disasters.")
        return disasters
    
    except Exception as e:
        print("Error loading existing disasters:", e)
        return []
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# link disaster id to each post
def update_bluesky_disaster_column(post_to_disaster):
    try:
        print("Updating temp_bluesky disaster column...")
        conn = get_db_connection()
        cursor = conn.cursor()

        for post_id, disaster_id in post_to_disaster:
            cursor.execute("""
                UPDATE temp_bluesky
                SET disaster_id = %s
                WHERE Post_ID = %s;
            """, (disaster_id, post_id))

        conn.commit()

        print("temp_bluesky disaster column updated successfully.")
    except Exception as e:
        print("Error updating raw_bluesky disaster column:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# remove posts without a cluster
def remove_noise_post(post_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM temp_bluesky WHERE post_id = %s;
        """, (post_id,))
        post_data = cursor.fetchone()

         # log noise to drop for error checking
        with open("noise_posts.txt", "a", encoding="utf-8") as f:
            f.write(f"\npost id: {post_data[0]}\n")
            f.write(f"post text: {post_data[1]}\n")
        
        cursor.execute("""
            DELETE FROM temp_bluesky WHERE post_id = %s;
        """, (post_id,))
        conn.commit()
    except Exception as e:
        print(f"Error handling post id {post_id}:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# insert new disasters into disaster information
def insert_new_disaster(name, location_name, centroid, lat, long, radius, date, summary):
    try:
        print(f"Inserting new disaster: {name}...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO disaster_information 
            (name, location_name, centroid, lat, long, radius, date, summary)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (name, location_name, centroid.tolist(), lat, long, radius, date, summary))
        disaster_id = cursor.fetchone()[0]
        conn.commit()
        print(f"New disaster {name} inserted with ID {disaster_id}.")
        return disaster_id
    except Exception as e:
        print("Error inserting new disaster:", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# insert updated centroids into disaster information row
def update_disaster_centroid(disaster_id, new_centroid):
    try:
        print(f"Updating centroid for disaster {disaster_id}...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE disaster_information
            SET centroid = %s
            WHERE id = %s;
        """, (new_centroid.tolist(), disaster_id))
        conn.commit()
        print(f"Centroid for disaster {disaster_id} updated.")
    except Exception as e:
        print(f"Error updating centroid for disaster {disaster_id}:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# pull unclustered posts
def get_unprocessed_posts():
    try:
        print("Fetching unprocessed posts...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Post_ID, Post_Original_Text 
            FROM temp_bluesky 
            WHERE disaster_id IS NULL;
        """)
        
        posts = cursor.fetchall()
        print(f"Fetched {len(posts)} unprocessed posts.")
        return posts
    
    except Exception as e:
        print("Error fetching unprocessed posts:", e)
        return []
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Helper function to update centroids with weighted averaging
def update_disaster_centroid_weighted(disaster_id, embedding, conn=None):
    """Update disaster centroid with a new embedding using weighted averaging."""
    try:            
        print(f"updating centroid for disaster {disaster_id}")
        conn = get_db_connection()
        cursor = conn.cursor()
        # Get current centroid and count of posts in this disaster
        cursor.execute("""
            SELECT centroid, 
                  (SELECT COUNT(*) FROM temp_bluesky WHERE disaster_id = %s) as post_count
            FROM disaster_information 
            WHERE id = %s
        """, (disaster_id, disaster_id))
        
        result = cursor.fetchone()
        if not result:
            print(f"Warning: Disaster {disaster_id} not found in database.")
            return
            
        current_centroid, post_count = result
        current_centroid = np.array(current_centroid)
        
        # Weight based on number of posts
        # New centroid = (current_centroid * post_count + new_embedding) / (post_count + 1)
        if post_count > 0:
            updated_centroid = (current_centroid * post_count + embedding) / (post_count + 1)
        else:
            updated_centroid = embedding
            
        # Update in database
        cursor.execute("""
            UPDATE disaster_information
            SET centroid = %s
            WHERE id = %s
        """, (updated_centroid.tolist(), disaster_id))
        
        conn.commit()
        print(f"Updated centroid for disaster {disaster_id} with weighted averaging.")
        
    except Exception as e:
        print(f"Error updating centroid for disaster {disaster_id}:", e)
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()