# ---------------------------------------------------------------------------------------------------------
# THIS FILE DEFINES A MULTICLASSIFIER THAT MATCHES THE AVERAGE OF A POSTS TEXT FEATURES TO A SPECIFIC CLASS
# ---------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import re, os, pickle
from gensim.models import KeyedVectors
import gensim.downloader as api
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.exceptions import UndefinedMetricWarning
import warnings

warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

# directory of the current script
script_dir = os.path.dirname(__file__)
DATA_DIR = "../../data/datasets"

# get train/test data
train_path = os.path.join(script_dir, DATA_DIR, 'train.tsv')
test_path = os.path.join(script_dir, DATA_DIR, 'test.tsv')
train = pd.read_csv(train_path, sep="\t").groupby("event_type").sample(frac=1)
test = pd.read_csv(test_path, sep="\t").groupby("event_type").sample(frac=1)

# Download the model 
model_path = os.path.join(script_dir, "word2vec-google-news-300.model")

if os.path.exists(model_path):
    word2vec_model = KeyedVectors.load(model_path)
else: 
    path = api.load("word2vec-google-news-300", return_path=True)
    word2vec_model = KeyedVectors.load_word2vec_format(path, binary=True)
    word2vec_model.save(model_path)

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

# extract word embeddings from the train/test data
train_embeddings = np.array([preprocess_with_embeddings(text, word2vec_model) for text in train['tweet_text']])
test_embeddings = np.array([preprocess_with_embeddings(text, word2vec_model) for text in test['tweet_text']])

# convert event_type to integers
labels = train['event_type'].factorize()[0]
actual_y = test["event_type"].factorize()[0]

# train the classifier
model = LinearSVC()
model.fit(train_embeddings, labels)
predicted_y = model.predict(test_embeddings)

# performance report
print(classification_report(actual_y, predicted_y, target_names=test["event_type"].unique()))

# save model
filename = os.path.join(script_dir, "word2vec_multiclass_model.sav")
pickle.dump(model, open(filename, 'wb'))