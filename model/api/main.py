from fastapi import FastAPI 
from pydantic import BaseModel 
import joblib 
from model_helpers import preprocess, analyze_sentiment

LABEL_MAP = {
    0: "earthquake", 
    1: "wildfire", 
    2: "flood", 
    3: "hurricane", 
    4: "unrelated"
}

app = FastAPI() 

# Load disaster-type classifier
file = "optimized_model.sav"
model = joblib.load(file)

# Define input schema 
class PostInput(BaseModel): 
    text: str 

# Define output schemas
class PredictionOutput(BaseModel): 
    event_type: str 

class SentimentOutput(BaseModel): 
    sentiment_score: float

@app.get("/")
def read_root(): 
    return {"message": "Model prediction API"}

# Health route to keep service warm
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict-disaster", response_model=PredictionOutput)
def predict_event_type(data: PostInput):
    text = [preprocess(data.text)]
    predicted_class = model.predict(text)[0] # Returns value from [0...4]
    predicted_label = LABEL_MAP.get(int(predicted_class), "unknown") # Convert class to string value

    return {"event_type": predicted_label}    

@app.post("/predict-sentiment", response_model=SentimentOutput)
def predict_sentiment(data: PostInput): 
    score = analyze_sentiment(preprocess(data.text))

    return {"sentiment_score": score}