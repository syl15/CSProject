import pandas as pd
import psycopg2
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
import plotly.express as px
from database import get_db_connection

def pull():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    temp_bluesky.post_id, 
                    temp_bluesky.post_original_text, 
                    disaster_information.name
                FROM 
                    temp_bluesky
                JOIN 
                    disaster_information 
                ON 
                    temp_bluesky.disaster_id = disaster_information.id;
                """)
            results = cursor.fetchall()
            return pd.DataFrame(results, columns=["post_id", "post_text", "disaster_name"])
        else:
            print("❌ Could not connect to database.")
    except Exception as e:
        print("Error creating table:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()  

df = pull()

if not df.empty:
    # Step 2: Embed the post texts
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df['post_text'].tolist(), show_progress_bar=True)

    # Step 3: UMAP projection to 2D
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric='euclidean', random_state=42)
    projection = reducer.fit_transform(embeddings)
    df['x'] = projection[:, 0]
    df['y'] = projection[:, 1]

    # Step 4: Visualize clusters by disaster_id
    fig = px.scatter(
        df,
        x='x',
        y='y',
        color="disaster_name",
        hover_data=['post_id', 'post_text'],
        title='Bluesky Posts Clustered into Disasters',
        labels={
        "x": "UMAP Dimension 1",
        "y": "UMAP Dimension 2",
        "disaster_name": "Disaster Name"
    }
    )

    fig.update_layout(
    legend_title="Disaster Name",
    width=500,
    height=800
)
    fig.show()
else:
    print("⚠️ No data to visualize.")