from flask import Flask 
from run_pipeline import run_pipeline 
from config import get_deployed_fastapi_link
import requests
import time
import traceback
import os

BASE_URL = get_deployed_fastapi_link()

FASTAPI_HEALTH_URL = BASE_URL + "/health"
PREDICT_DISASTER_URL = BASE_URL + "/predict-disaster"
PREDICT_SENTIMENT_URL = BASE_URL + "/predict-sentiment"

MAX_RETRIES = 5
RETRY_DELAY = 10

app = Flask(__name__) 

SAMPLE_TEXT = {"text": "Test post for endpoint readiness"}

@app.get("/")
def home():
    return "Trigger Pipeline App"

@app.get("/health")
def health_check():
    return {"status": "OK"}, 200

@app.route("/trigger-pipeline", methods=["POST"])
def trigger_pipeline(): 
    for attempt in range(1, MAX_RETRIES + 1): 
        try: 
            # Step 1: Check FastAPI health 
            print(f"\n--- FastAPI readiness check: attempt {attempt} ---")
            t0 = time.time()

            # Dynamic timeouts
            timeout_health = 30 if attempt == 1 else 15
            timeout_disaster = 50 if attempt == 1 else 30
            timeout_sentiment = 50 if attempt == 1 else 20

            # /health
            t1 = time.time()
            health = requests.get(FASTAPI_HEALTH_URL, timeout=timeout_health)
            health_time = time.time() - t1
            print(f"/health responded in {health_time:.2f}s")

            # /predict-disaster
            t2 = time.time()
            disaster = requests.post(PREDICT_DISASTER_URL, json=SAMPLE_TEXT, timeout=timeout_disaster)
            disaster_time = time.time() - t2
            print(f"/predict-disaster responded in {disaster_time:.2f}s")

            # /predict-sentiment
            t3 = time.time()
            sentiment = requests.post(PREDICT_SENTIMENT_URL, json=SAMPLE_TEXT, timeout=timeout_sentiment)
            sentiment_time = time.time() - t3
            print(f"/predict-sentiment responded in {sentiment_time:.2f}s")

            total_time = time.time() - t0

            # Step 2: Run pipeline 
            if health.status_code == 200 and disaster.status_code == 200 and sentiment.status_code == 200:
                run_pipeline()
                return {
                    "status": "Pipeline triggered successfully",
                    "fastapi_response_time_sec": round(total_time, 2),
                    "individual_times_sec": {
                        "health": round(health_time, 2),
                        "predict_disaster": round(disaster_time, 2),
                        "predict_sentiment": round(sentiment_time, 2),
                    }
                }, 200
            else:
                print(f"Unexpected status codes: health={health.status_code}, "f"disaster={disaster.status_code}, sentiment={sentiment.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Health check attempt {attempt} failed: {e}")
            traceback.print_exc()
        
        if attempt < MAX_RETRIES: 
            print(f"Retrying in {RETRY_DELAY * attempt} seconds")
            time.sleep(RETRY_DELAY * attempt)

    return {"error": f"FastAPI service is down after {MAX_RETRIES} retries"}, 503

if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=False)