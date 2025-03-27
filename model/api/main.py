from fastapi import FastAPI 
from pydantic import BaseModel 
import joblib 

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

# Define output schema 
class PredictionOutput(BaseModel): 
    event_type: str 

@app.get("/")
def read_root(): 
    return {"message": "Model prediction API"}

@app.post("/predict", response_model=PredictionOutput)
def predict_event_type(data: PostInput): 
    # Get text from input data 
    text = [data.text]

    # Make a prediction 
    predicted_class = model.predict(text)[0] # Returns value from [0...4]
    predicted_label = LABEL_MAP.get(int(predicted_class), "unknown") # Convert class to string value

    # Return event type 
    return {"event_type": predicted_label}