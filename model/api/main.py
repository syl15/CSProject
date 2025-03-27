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
    predicted_label = str(model.predict(text)[0])

    # Return event type 
    return {"event_type": predicted_label}