import numpy as np
import psycopg2
from bluesky_clustering import embed_posts  # Replace with actual import
from database import get_db_connection   # Replace with your DB connection function

def update_all_disaster_centroids():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Step 1: Get all disaster IDs
        cursor.execute("SELECT id FROM disaster_information")
        disaster_ids = [row[0] for row in cursor.fetchall()]
        
        print(f"Found {len(disaster_ids)} disasters to update.")

        for disaster_id in disaster_ids:
            print(f"\nProcessing disaster ID: {disaster_id}")
            
            # Step 2: Get all (post_id, post_original_text) for this disaster
            cursor.execute("""
                SELECT post_id, post_original_text 
                FROM temp_bluesky 
                WHERE disaster_id = %s
            """, (disaster_id,))
            posts = cursor.fetchall()
            
            if not posts:
                print(f"No posts found for disaster {disaster_id}, skipping.")
                continue
            
            # Step 3: Get normalized embeddings for all posts
            embeddings = embed_posts(posts)
            if embeddings.size == 0:
                print(f"Skipping disaster {disaster_id} due to embedding failure.")
                continue
            
            # Step 4: Compute centroid
            new_centroid = np.mean(embeddings, axis=0)
            
            # Step 5: Update in DB
            cursor.execute("""
                UPDATE disaster_information
                SET centroid = %s
                WHERE id = %s
            """, (new_centroid.tolist(), disaster_id))
            conn.commit()
            print(f"Updated centroid for disaster {disaster_id}")
            
    except Exception as e:
        print("Error during centroid update:", e)
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

update_all_disaster_centroids()