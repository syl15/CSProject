from fastapi import FastAPI 
from pydantic import BaseModel 
import joblib 
import requests 

app = FastAPI() 

# Load dummy model 
# TODO: replace line 9 with line 10 when Katrina decodes her ints to strings 
model = joblib.load("dummy_model.pkl")
# model = joblib.load("optimized_model.sav")

# Define input schema 
class TweetInput(BaseModel): 
    text: str 

# Output schema 
class PredictionOutput(BaseModel): 
    event_type: str 

@app.get("/")
def read_root(): 
    return {"message": "Event Type Prediction API"}

# TODO: update this once we actually have the model
@app.post("/predict", response_model=PredictionOutput)
def predict_event_type(data: TweetInput): 
    # Get text from input data 
    text = [data.text]

    # Make a prediction 
    predicted_label = str(model.predict(text)[0])

    # Return event type 
    return {"event_type": predicted_label}