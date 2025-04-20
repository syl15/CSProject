import re
import pandas as pd
import nltk
from sklearn.exceptions import UndefinedMetricWarning
import warnings

# ------------------ Setup ------------------

# If you get SSL errors on Mac, run:
# /Applications/Python\ 3.x/Install\ Certificates.command globally (OUTSIDE your venv)
# Replace '3.x' with your version (ex. /Applications/Python\ 3.12/Install\ Certificates.command)


# ------------------ TFIDF Preprocessing ------------------
nltk.download("wordnet", quiet=True)
from nltk.stem import WordNetLemmatizer as lemma
def preprocess(text):
    text = re.sub(r'https?:\/\/\S*', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', '', text)
    text = " ".join([word for word in text.split() if word[0] != "@" and word.isalpha()])
    text = " ".join([lemma().lemmatize(token) for token in text.split()]).strip()
    return text


# ------------------ Sentiment Analysis ------------------
# Download VADER lexicon 
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()
def analyze_sentiment(text):
    scores = sia.polarity_scores(text)
    return scores["compound"]


# ------------------ Testing Locally ------------------
if __name__ == "__main__":
    posts = pd.read_csv("../../data/datasets/test.tsv", sep="\t").sample(n=10)
    for post_text in posts["tweet_text"]:
        score = analyze_sentiment(preprocess(post_text))
        print(score, post_text)