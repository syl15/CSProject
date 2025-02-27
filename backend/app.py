import sys
from flask import Flask
from populate import raw_crisis_nlp_populate

app = Flask(__name__)

@app.get("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    reset_db = "--reset-db" in sys.argv # optional argument to delete and repopulate raw_crisis_nlp_ table

    if reset_db:
        print("🔄 resetting and repopulating Raw_Crisis_NLP table...")
    else:
        print("Checking if Raw_Crisis_NLP table needs to be populated...")
        
    raw_crisis_nlp_populate(reset=reset_db)