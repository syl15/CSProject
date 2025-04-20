import pandas as pd
import numpy as np
import re, os, pickle, joblib

from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

from tqdm.auto import tqdm
from sentence_transformers import SentenceTransformer

# allow importing of model_helpers.py from ../api
# import sys
# sys.path.insert(1, os.path.join(sys.path[0], '..'))
# from api.model_helpers import preprocess

DATA_DIR = "../../data/datasets"
filename = "st_model.sav"

transformer = SentenceTransformer("paraphrase-albert-small-v2")

# ------------------ Sentence Transformer Preprocessing ------------------
# don't use standard preprocessing techniques (uncasing/lemmatizing) on pretrained models
def preprocess(text, transformer):
    text = re.sub(r'https?:\/\/\S*', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', '', text)
    text = " ".join([word for word in text.split() if word[0] != "@" and word.isalpha()])
    text = transformer.encode(text)
    return text

# train the model and generate the .sav file
def generate():
	model = LinearSVC(class_weight="balanced")

	train = pd.read_csv(os.path.join(DATA_DIR, "train.tsv"), sep="\t").groupby("event_type").sample(frac=0.25)
	train_embeddings = np.array([preprocess(text, transformer) for text in tqdm(train["tweet_text"])])
	labels, label_names = train["event_type"].factorize()
	model.fit(train_embeddings, labels)

	with open(filename, "wb") as f:
		pickle.dump((model, label_names), f)

# analyze model accuracy against test data (test against a whole dataset)
def analyze(dataset):
	model, label_names = joblib.load(filename)

	test = pd.read_csv(os.path.join(DATA_DIR, dataset), sep="\t").groupby("event_type").sample(frac=0.25)
	test_embeddings = np.array([preprocess(text, transformer) for text in tqdm(test["tweet_text"])])

	# convert event_type to integers
	actual_y = test["event_type"].factorize()[0]
	predicted_y = model.predict(test_embeddings)

	print(classification_report(actual_y, predicted_y, target_names=label_names))

# test model against a single example tweet
def test(text):
	model, label_names = joblib.load(filename)
	prediction = model.predict([preprocess(text, transformer)])[0]
	print(label_names[prediction])

generate()
analyze("final_test.tsv")