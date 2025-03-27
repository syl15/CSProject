from fastapi import FastAPI 
from pydantic import BaseModel 
import joblib 
import requests 

app = FastAPI() 

# Load dummy model 
model = joblib.load("optimized_model.sav")

# Define input schema 
class PostInput(BaseModel): 
    text: str 

# Output schema 
class PredictionOutput(BaseModel): 
    event_type: str 

@app.get("/")
def read_root(): 
    return {"message": "Event Type Prediction API"}

LABEL_MAP = {
    0: "earthquake", 
    1: "fire", 
    2: "flood", 
    3: "hurricane", 
    4: "unrelated"
}

@app.post("/predict", response_model=PredictionOutput)
def predict_event_type(data: PostInput): 
    # Get text from input data 
    text = [data.text]

    # Make a prediction 
    predicted_class = model.predict(text)[0] # Returns value from [0...4]
    predicted_label = LABEL_MAP.get(int(predicted_class), "unknown") # Convert class to string value

    # Return event type 
    return {"event_type": predicted_label}


# Get posts from bluesky and classify them
# NOTE: This will be the classification logic 
FLASK_API_URL = "http://127.0.0.1:5001/unclassified-posts"

@app.get("/bluesky-data") # TODO: change name to /classify 
def batch_classify(): 
    """
    Pulls unclassified posts from Flask, classifies them, and returns predictions
    """
    try: 
        # 1. Get unclassified posts from Flask 
        response = requests.get(FLASK_API_URL)
        if response.status_code != 200: 
            return {"error": "Failed to fetch unclassified posts"}

        posts = response.json() 
        print(posts)
        
        # 2. Run model prediction on each 
        # NOTE: Run through event classifier AND sentiment classifier before returning
        '''
        results = [] 
        for post in posts: 
            prediction = model.predict([post["post_original_text"]])[0]
            results.append({
                "post_id": post["post_id"], 
                "post_original_text": post["post_original_text"],
                "model_disaster_label": prediction
            })
        
        return results
        '''

        # 3. POST results back to Flask 
        # TODO: Add a route in Flask to receive classified-posts 
        # TODO: Add logic here to post final results

        return posts # Return temporarily, return actual results later

    except Exception as e: 
        return {"error" : str(e)}
