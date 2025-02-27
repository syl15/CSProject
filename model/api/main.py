from fastapi import FastAPI 
from pydantic import BaseModel 
import joblib 

app = FastAPI() 

# Load dummy model 
model = joblib.load("dummy_model.pkl")

# Define input schema 
class TweetInput(BaseModel): 
    text: str 

# Output schema 
class PredictionOutput(BaseModel): 
    event_type: str 

@app.get("/")
def read_root(): 
    return {"message": "Event Type Prediction API"}

@app.post("/predict", response_model=PredictionOutput)
def predict_event_type(data: TweetInput): 
    # Get text from input data 
    text = [data.text]

    # Make a prediction 
    predicted_label = model.predict(text)[0]

    # Return event type 
    return {"event_type": predicted_label}