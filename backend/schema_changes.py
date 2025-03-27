from database import get_db_connection 

def change_schema(): 
    try: 
        conn = get_db_connection() 
        cursor = conn.cursor()

        # Add model_disaster_label if does not already exist 
        cursor.execute('''
            ALTER TABLE raw_bluesky 
            ADD COLUMN IF NOT EXISTS model_disaster_label TEXT; 
        ''')

        # TODO: add model_sentiment_label if does not already exist
        # TODO: add model_sentiment_score if does not already exist

        conn.commit() 
        print("Successfully applied changes.")
    except Exception as e: 
        print("Failed to apply changes:", e)
    finally: 
        if cursor: 
            cursor.close() 
        if conn: 
            conn.close()

if __name__ == "__main__": 
    change_schema()