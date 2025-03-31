from fastapi import FastAPI 
from pydantic import BaseModel 
import joblib 
from api_helpers import preprocess, analyze_sentiment

LABEL_MAP = {
    0: "earthquake", 
    1: "fire", 
    2: "flood", 
    3: "hurricane", 
    4: "unrelated"
}

app = FastAPI() 

# Load disaster-type classifier
model = joblib.load("optimized_model.sav")

# Define input schema 
class PostInput(BaseModel): 
    text: str 

# Define output schemas
class PredictionOutput(BaseModel): 
    event_type: str 

class SentimentOutput(BaseModel): 
    sentiment_score: int

@app.get("/")
def read_root(): 
    return {"message": "Model prediction API"}

@app.post("/predict-disaster", response_model=PredictionOutput)
def predict_event_type(data: PostInput): 
    # Get text from input data 
    text = [preprocess(data.text)]

    # Make a prediction 
    predicted_label = str(model.predict(text)[0])

    # Return event type 
    return {"event_type": predicted_label}

@app.post("/predict-sentiment", response_model=SentimentOutput)
def predict_sentiment(data: PostInput): 
    score = analyze_sentiment(preprocess(data.text))

    # Return sentiment_score 
    return {"sentiment_score": score}
