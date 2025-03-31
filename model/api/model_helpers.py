import re

nlp = spacy.load('en_core_web_sm')
def preprocess(text):
    text = re.sub(r'https?:\/\/\S*', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = " ".join([word for word in text.split() if word[0] != "@"])
    text = text.lower()
    text = " ".join([token.lemma_ for token in nlp(text)])
    return text

import pandas as pd
import nltk
from sklearn.exceptions import UndefinedMetricWarning
import warnings

# If you get SSL errors on Mac, run:
# /Applications/Python\ 3.x/Install\ Certificates.command globally (OUTSIDE your venv)
# Replace '3.x' with your version (ex. /Applications/Python\ 3.12/Install\ Certificates.command)

nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

# Initialize the analyzer once
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    scores = sia.polarity_scores(text)
    return scores["compound"]

###### Test the sentiment analysis model ######
# test = pd.read_csv("../datasets/test.tsv", sep="\t").sample(n=10)
# for i in test["tweet_text"]:
#     score = analyze_sentiment(i)
#     print(score, i)