import pandas as pd
import numpy as np
import os, re

DATA_DIR = "datasets"
train = pd.read_csv(os.path.join(DATA_DIR, "train.tsv"), sep="\t").groupby("event_type").sample(frac=1)
test = pd.read_csv(os.path.join(DATA_DIR, "test.tsv"), sep="\t").groupby("event_type").sample(frac=1)

import nltk
nltk.download("wordnet", quiet=True)
from nltk.stem import WordNetLemmatizer as lemma
def preprocess(text):
    text = re.sub(r'https?:\/\/\S*', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', '', text)
    text = " ".join([word for word in text.split() if word[0] != "@" and word.isalpha()])
    text = text.lower()
    text = " ".join([lemma().lemmatize(token) for token in text.split()]).strip()

    return text

from sklearn import metrics
from sklearn.metrics import classification_report, make_scorer, f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
models = [
    xgb.XGBClassifier(random_state=42),
    RandomForestClassifier(random_state=42),
    MultinomialNB(),
    LogisticRegression(random_state=42, solver="liblinear"),
    LinearSVC(class_weight="balanced"),
]

paramss = [
    {
        "tfidf__ngram_range": [(1, 1), (1, 2)],
        "tfidf__max_df": [0.75, 0.8, 0.9, 0.95],
        "tfidf__min_df": [0.1, 0.01],
        # "tfidf__use_idf": [True, False],
        # "tfidf__binary": [True, False],
        "clf__max_depth": [5, 6, 7, 8],
        "clf__n_estimators": [10, 50],
        "clf__learning_rate": [1, 0.1, 0.01, 0.001]
    },
    {
        "tfidf__ngram_range": [(1, 1), (1, 2)],
        "tfidf__max_df": [0.75, 0.8, 0.9, 0.95],
        "tfidf__min_df": [0.1, 0.01],
        'clf__n_estimators': [100, 200, 500],
        'clf__max_features': ['sqrt', 'log2'],
        'clf__max_depth' : [3,5,7]
    },
    {
        "tfidf__ngram_range": [(1, 1), (1, 2)],
        "tfidf__max_df": [0.75, 0.8, 0.9, 0.95],
        "tfidf__min_df": [0.1, 0.01],
        'clf__alpha': [0.1, 0.5, 1.0]
    },
    {
        "tfidf__ngram_range": [(1, 1), (1, 2)],
        "tfidf__max_df": [0.75, 0.8, 0.9, 0.95],
        "tfidf__min_df": [0.1, 0.01],
        "clf__C": np.logspace(-3,3,7),
        "clf__penalty":["l1","l2"]
    },
    {
        "tfidf__ngram_range": [(1, 1), (1, 2)],
        "tfidf__max_df": [0.75, 0.8, 0.9, 0.95],
        "tfidf__min_df": [0.1, 0.01],
        "clf__C": [0.01, 100, 1, 0.1, 10],
    }
]

# tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, ngram_range=(1, 10), stop_words="english")
tfidf = TfidfVectorizer(sublinear_tf=True, stop_words="english")
features = train["tweet_text"].apply(preprocess)
labels = train["event_type"].factorize()[0]

scoring = {'f1':make_scorer(f1_score, average="weighted"),
    # 'precision':'precision',
    # 'roc_auc':'roc_auc',
    # 'recall':'recall'
}


for model, params in zip(models, paramss):
    pipeline = Pipeline([
        ('tfidf', tfidf),
        ('clf', model)
    ])

    clf = GridSearchCV(
        pipeline,
        params,
        cv=5,
        scoring=scoring,
        refit = 'f1',
        verbose=10,
        n_jobs=1,
        pre_dispatch = '1 * n_jobs',
        error_score=-1
    ) # Using 5-fold cross-validation

    clf.fit(features, labels)

    print("model name: ", model.__class__.__name__)
    print("best parameters: ", clf.best_params_)

    actual_y = test["event_type"].factorize()[0]
    predicted_y = clf.best_estimator_.predict(test["tweet_text"].apply(preprocess))
    print(classification_report(actual_y, predicted_y, target_names=test["event_type"].unique()))