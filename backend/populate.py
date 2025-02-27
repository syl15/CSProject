'''
The purpose of this file is to populate the Raw_Crisis_NLP table with the Crisis NLP data
from /train.tsv

This file will execute if app.py is run with the --reset-db flag or if the db is not populated
'''

import csv
from database import get_db_connection

TSV_FILE = "../data/train.tsv"

'''populate the raw crisis nlp table or reset it'''
def raw_crisis_nlp_populate(reset=False):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        table_name = "Raw_Crisis_NLP"

        # create the table if it doesn't exist
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                Tweet_ID BIGINT PRIMARY KEY,
                Tweet_Original_Text TEXT,
                Class_Label TEXT,
                Event_Type TEXT,
                Specific_Event_Name TEXT
            );
        ''')
        conn.commit()
        print(f"✅ {table_name} table is ready.")

        if reset:
            cursor.execute(f"DELETE FROM {table_name};")
            print(f"✅ {table_name} data deleted.")

        # add crisis data if the table is empty
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]

        if row_count == 0 or reset:
            with open(TSV_FILE, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter='\t')
                next(reader)  # skip header row 
                for row in reader:
                    # print(row)
                    cursor.execute(f"""
                        INSERT INTO {table_name} (Tweet_ID, Tweet_Original_Text, Class_Label, Event_Type, Specific_Event_Name) 
                        VALUES (%s, %s, %s, %s, %s);
                    """, row)

            conn.commit()
            print(f"✅ {table_name} successfully populated.")

        else:
            print(f"{table_name} already has data. Skipping population.")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()   

if __name__ == "__main__":
    raw_crisis_nlp_populate()