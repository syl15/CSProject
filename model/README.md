# Model 

## Core Contents 
- `/api` directory: contains all files relevant to running the FastAPI app
  - `main.py`: entry point for FastAPI app, handles the routes `/predict-disaster` and `/predict-sentiment`
- `/experimentation` directory: contains files relevant to other tested but undeployed models
  - `model_st.py` - This model uses a pretrained sentence transformer model to generate embeddings.
    - trained on a random sample from `data/scripts/datasets/train.tsv` that is 1/4 the size of the full dataset for the optimal balance of accuracy and resources
    - uses the `paraphrase-albert-small-v2` pretrained model
    - generates `st_model.sav`

## Prerequisites 
- If you don't have a `.sav` file in your `/api` folder, you need to run the appropriate `model.py` file or equivalent to generate the model binary and ensure that it's in the `/api` directory
- Do the same to test the two models in `/experimentation`

## Using the FastAPI routes 

1. Activate your `venv` and install dependencies; see `backend/README.MD` for full instructions 
2. Run the FastAPI app: </br>
    `cd model/api` </br>
    `python main.py` </br>
    `uvicorn main:app --reload`
3. View the local endpoint: `http://127.0.0.1:8000`
    - To use test the endpoint, you can go to `http://127.0.0.1:8000/docs`, which is an interactive SwaggerUI page that will display all the available routes. 
    - Alternatively, use [curl commands](#sample-curl-command-for-testing) in your terminal

### Overview of API routes 

`POST /predict-disaster`
- Takes in text input and outputs one of the following disaster event types: hurricane, earthquake, wildfire, flood, unrelated. 
  
`POST /predict-sentiment`
- Takes in text input and outputs a sentiment score from -1 to 1.

### Sample curl commands for testing 

* `curl -X POST http://localhost:8000/predict-disaster -H "Content-Type: application/json" -d '{"text": "Tornado warning in Oklahoma"}'`
* (for windows command prompt) `curl -X POST http://localhost:8000/predict-disaster -H "Content-Type: application/json" -d "{\"text\": \"Tornado warning in Oklahoma\"}"`


Expected response: `{"event_type":"tornado"}` 


