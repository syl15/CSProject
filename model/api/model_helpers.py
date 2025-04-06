import re
import spacy
import spacy.util 
import subprocess 
import sys
import numpy as np
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

# ------------------ TFIDF Preprocessing ------------------

def preprocess(text):
    text = re.sub(r'https?:\/\/\S*', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = " ".join([word for word in text.split() if word[0] != "@"])
    text = text.lower()
    text = " ".join([token.lemma_ for token in nlp(text)])
    
    return text

# ------------------ Embeddings Preprocessing ------------------
# return the average embedding for a text based on Word2Vec embeddings
def get_word_embeddings(text, model, vector_size=300):
    words = text.split()
    embeddings = []

    for word in words: # ignores words w/out embeddings in Word2Vec
        if word in model:
            embeddings.append(model[word])

    # if no embeddings found, return a vector of zeros
    if not embeddings:
        return np.zeros(vector_size)
    
    # return average of the embeddings in the post
    return np.mean(embeddings, axis=0)

def preprocess_with_embeddings(text, model):

    text = re.sub(r'https?:\/\/\S*', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = " ".join([word for word in text.split() if word[0] != "@"])
    text = text.lower()
    
    return get_word_embeddings(text, model)

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