from fastapi import FastAPI 
from pydantic import BaseModel 
import joblib 
from model_helpers import preprocess, preprocess_with_embeddings, analyze_sentiment
from gensim.models import KeyedVectors

LABEL_MAP = {
    0: "earthquake", 
    1: "fire", 
    2: "flood", 
    3: "hurricane", 
    4: "unrelated"
}

app = FastAPI() 

# Load disaster-type classifier
''' word2vec_multiclass_model.sav represents the word2vec + linearSVC model
    optimized.sav represents the TFDIF + linearSVC model
'''
# file = "word2vec_multiclass_model.sav"
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

@app.post("/predict-disaster", response_model=PredictionOutput)
def predict_event_type(data: PostInput):
    if (file == "optimized_model.sav"):
        text = [preprocess(data.text)]

    elif (file == "word2vec_multiclass_model.sav"):
        word2vec_model = KeyedVectors.load("../word2vec-google-news-300.model")
        text = [preprocess_with_embeddings(data.text, word2vec_model)]

    else:
        None

    predicted_class = model.predict(text)[0] # Returns value from [0...4]
    predicted_label = LABEL_MAP.get(int(predicted_class), "unknown") # Convert class to string value

    return {"event_type": predicted_label}    


@app.post("/predict-sentiment", response_model=SentimentOutput)
def predict_sentiment(data: PostInput): 
    score = analyze_sentiment(preprocess(data.text))

    # Return sentiment_score 
    return {"sentiment_score": score}