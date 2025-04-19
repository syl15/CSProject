# this script generates a test dataset made from completely unseen-before data to assess the true accuracy of the model
# DATA SOURCES:
# 1. disaster: https://huggingface.co/datasets/QCRI/CrisisMMD/viewer/damage?views%5B%5D=damage_train
# 2. non-disaster/unrelated only from: https://www.kaggle.com/datasets/vstepanenko/disaster-tweets (already downloaded to datasets/tweets.csv)
# 3. disaster: related disasters only (unrelated may overlap with unrelated from test data): https://huggingface.co/datasets/nlp-pw/Disaster-Tweets-Normalized/

import pandas as pd
from datasets import load_dataset, concatenate_datasets, Value

DATA_DIR = "../datasets"
datasets = []
keep_columns = ["tweet_text", "event_type"]

# PART 1
data = load_dataset("QCRI/CrisisMMD", "damage", split="train")

label_map = {
    "hurricane_harvey": "hurricane",
    "iraq_iran_earthquake": "earthquake",
    "hurricane_irma": "hurricane",
    "hurricane_maria": "hurricane",
    "california_wildfires": "wildfire",
    "mexico_earthquake": "earthquake",
    "srilanka_floods": "flood"
}
data = data.map(lambda row: {"event_name": label_map[row["event_name"]]}).rename_column("event_name", "event_type")
datasets.append(data)

# PART 2
data = load_dataset("csv", data_files=f"{DATA_DIR}/tweets.csv", split="train")
data = data.filter(lambda row: row["target"] == 0).rename_column("text", "tweet_text").map(lambda row: {"target": "unrelated"}).rename_column("target", "event_type")
datasets.append(data)

# PART 3
data = load_dataset("nlp-pw/Disaster-Tweets-Normalized", split="test")
data = data.filter(lambda row: row["disaster_type"] != "unrelated").rename_column("disaster_type", "event_type")
datasets.append(data)

# CONCATENATE
SAMPLE_SIZE = 2000 # n from each dataset 
for n, dataset in enumerate(datasets):
    datasets[n] = dataset.select_columns(keep_columns).shuffle().select(range(SAMPLE_SIZE))
final_dataset = concatenate_datasets(datasets)
df = pd.DataFrame(final_dataset)
freqs = df["event_type"].value_counts()
print(df)
print(freqs)

final_dataset.to_csv(f"{DATA_DIR}/final_test.tsv", sep="\t")