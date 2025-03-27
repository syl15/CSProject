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
    return round(scores["compound"] * 5)

# Optional: test the function when running this file directly 
if __name__ == "__main__": 
    test = pd.read_csv("../datasets/test.tsv", sep="\t").sample(n=10)
    for i in test["tweet_text"]:
        score = analyze_sentiment(i)
        print(score, i)