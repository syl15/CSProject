from fastapi import FastAPI 
from pydantic import BaseModel 
import joblib 
from sentiment_analysis import analyze_sentiment

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
    sentiment_score: int # scale: -5 to 5

@app.get("/")
def read_root(): 
    return {"message": "Model prediction API"}

@app.post("/predict-disaster", response_model=PredictionOutput)
def predict_event_type(data: PostInput): 
    # Get text from input data 
    text = [data.text]

    # Make a prediction 
    predicted_class = model.predict(text)[0] # Returns value from [0...4]
    predicted_label = LABEL_MAP.get(int(predicted_class), "unknown") # Convert class to string value

    # Return event type 
    return {"event_type": predicted_label}

@app.post("/predict-sentiment", response_model=SentimentOutput)
def predict_sentiment(data: PostInput): 
    score = analyze_sentiment(data.text)

    # Return sentiment_score 
    return {"sentiment_score": score}
