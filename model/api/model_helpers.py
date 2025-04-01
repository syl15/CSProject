import re
import spacy
import spacy.util 
import subprocess 
import sys
import pandas as pd
import nltk
from sklearn.exceptions import UndefinedMetricWarning
import warnings

# ------------------ Setup ------------------

# Installs 'en_core_web_sm' if it is already not
def install_spacy_model(model='en_core_web_sm'): 
    try: 
        spacy.load(model) 
    except OSError: 
        subprocess.run([sys.executable, "-m", "spacy", "download", model], check=True)

# Install and load the model 
install_spacy_model() 
nlp = spacy.load('en_core_web_sm')

# If you get SSL errors on Mac, run:
# /Applications/Python\ 3.x/Install\ Certificates.command globally (OUTSIDE your venv)
# Replace '3.x' with your version (ex. /Applications/Python\ 3.12/Install\ Certificates.command)

# Download VADER lexicon 
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

# ------------------ Preprocessing ------------------

def preprocess(text):
    text = re.sub(r'https?:\/\/\S*', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = " ".join([word for word in text.split() if word[0] != "@"])
    text = text.lower()
    text = " ".join([token.lemma_ for token in nlp(text)])
    return text

# ------------------ Sentiment Analysis ------------------

def analyze_sentiment(text):
    scores = sia.polarity_scores(text)
    return scores["compound"]

# ------------------ Testing Locally ------------------
if __name__ == "__main__":
    posts = pd.read_csv("../../data/datasets/test.tsv", sep="\t").sample(n=10)
    for post_text in posts["tweet_text"]:
        score = analyze_sentiment(preprocess(post_text))
        print(score, post_text)