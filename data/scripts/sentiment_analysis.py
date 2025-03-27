import pandas as pd
import nltk
from sklearn.exceptions import UndefinedMetricWarning
import warnings

# If you get SSL errors on Mac, run:
# /Applications/Python\ 3.x/Install\ Certificates.command globally (OUTSIDE your venv)
# Replace '3.x' with your version (ex. /Applications/Python\ 3.12/Install\ Certificates.command)

nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia

test = pd.read_csv("../datasets/test.tsv", sep="\t").sample(n=10)
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

def analyze_sentiment(text):
    scores = sia().polarity_scores(text)
    return round(scores["compound"] * 5)

for i in test["tweet_text"]:
    score = analyze_sentiment(i)
    print(score, i)