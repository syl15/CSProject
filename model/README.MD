### Testing the Dummy Model 

You will need three terminal windows to run Flask, FastAPI, and curl commands (to test). You will also need to have your venv activated and your requirements installed in each terminal before you start any of the apps. 

1. Start `main.py` (FastAPI app) in `model/api`
    - `cd model/api` 
    - `python main.py`
    - `uvicorn main:app --reload`
    - Should be running on `http://127.0.0.1:8000`
    - To test, go to `http://127.0.0.1:8000`
2. Start `app.py` (Flask app) in `backend`
    - `cd backend`
    - `python app.py`
    - Should be running on `http://127.0.0.1:5001`
3. Run curl commands (below)

**Example command:**

curl -X POST http://localhost:5001/predict \
     -H "Content-Type: application/json" \
     -d '{"text": "Tornado warning in Oklahoma"}'

curl -X POST http://localhost:5001/predict \
     -H "Content-Type: application/json" \
     -d '{"text": "Earthquake in Japan"}'

curl -X POST http://localhost:5001/predict \
     -H "Content-Type: application/json" \
     -d '{"text": "Had to evacuate because of the LA fires"}'

**Example response (in terminal):**
`{"event_type":"tornado"}`

No guarantees it's actually correct. The dummy model is pretty dumb. 

### Debugging 

If you don't see in any output, it could be due a variety of things, but I would recommend testing each service independently just to be sure. 

**Test FastAPI root endpoint:** 

curl http://localhost:8000/

Expected response: `{"message":"Event Type Prediction API"}`

**Test FastAPI prediction endpoint:** 

curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"text": "Tornado warning in Oklahoma"}'

Expected response: `{"event_type":"flood"}` (lol)

**Test mock Flask endpoint:**

curl -X POST http://localhost:5001/mock-predict \
     -H "Content-Type: application/json" \
     -d '{"text": "Hurricane warning in Florida"}'

Expected response: `{"event_type":"Testing Flask"}`
