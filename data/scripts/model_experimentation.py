import pandas as pd
import re
import spacy

train = pd.read_csv("datasets/train.tsv", sep="\t")
test = pd.read_csv("datasets/test.tsv", sep="\t")

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import cross_val_score
# from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer

models = [
    RandomForestClassifier(n_estimators=100, max_depth=5, random_state=0),
    MultinomialNB(),
    LogisticRegression(random_state=0),
    LinearSVC(),
]

nlp = spacy.load('en_core_web_sm')
def preprocess(text):
    text = re.sub(r'https?:\/\/\S*', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = " ".join([word for word in text.split() if word[0] != "@"])
    text = text.lower()
    text = " ".join([token.lemma_ for token in nlp(text)])
    return text

tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, ngram_range=(1, 10), stop_words='english')

features = tfidf.fit_transform(train["tweet_text"].apply(preprocess)).toarray()
test_features = tfidf.transform(test["tweet_text"].apply(preprocess)).toarray()
train["encoded_labels"] = train["event_type"].factorize()[0]
actual_y = test["event_type"].factorize()[0]
labels = train["encoded_labels"]

for model in models:
    model_name = model.__class__.__name__

    model.fit(features, labels)

    predicted_y = model.predict(test_features)

    print(model_name)
    print(metrics.classification_report(actual_y, predicted_y, target_names=test["event_type"].unique()))