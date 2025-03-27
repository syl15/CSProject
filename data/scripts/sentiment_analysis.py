import pandas as pd

test = pd.read_csv("datasets/test.tsv", sep="\t").sample(n=10)

from sklearn.exceptions import UndefinedMetricWarning
import warnings
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

import nltk
# nltk.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia

def analyze_sentiment(text):
    scores = sia().polarity_scores(text)
    return round(scores["compound"] * 5)

for i in test["tweet_text"]:
    score = analyze_sentiment(i)
    print(score, i)