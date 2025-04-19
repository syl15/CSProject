# combines specifically-labeled disaster data from crisisnlp with generally-labeled disaster data (which contains unrelated tweets) from huggingface
# also renames "fire" label to "wildfire"

import os
from datasets import load_dataset, concatenate_datasets, Value

DATA_DIR = "../datasets"

# tweets with unrelated data to insert into training and testing dataset
base_url = "https://huggingface.co/datasets/nlp-pw/Disaster-Tweets-Normalized/resolve/main/data/"
parquet_files = {'train': base_url+'train-00000-of-00001.parquet', 'test': base_url+'test-00000-of-00001.parquet'}

splits = parquet_files.keys()
unwanted_columns = ["hashtags", "emojis", "__index_level_0__"]

hf_dataset = {}
for split in splits:
    # remove unnecessary columns, rename disaster type column, and only include unrelated data
    hf_dataset[split] = load_dataset('parquet', data_files=parquet_files, split=split).remove_columns(unwanted_columns).rename_column("disaster_type", "event_type").filter(lambda row: row["event_type"] == "unrelated")

# split huggingface test dataset into test (0.5) and dev (0.5)
test_dev_split = hf_dataset["test"].train_test_split(test_size=0.5)
hf_dataset["test"] = test_dev_split["train"]
hf_dataset["dev"] = test_dev_split["test"]

for a, b in hf_dataset.items():
    # reformat unrelated dataset to fit shape of crisisnlp data: add class_label (keywords) column and populate with "None", add specific_event_name column and populate with "None", change datatype of tweet_id column
    hf_dataset[a] = b.add_column(name="class_label", column=("None" for i in range(len(b)))).add_column(name="specific_event_name", column=("None" for i in range(len(b)))).cast_column("tweet_id", Value("int64"))

# assuming combined crisisnlp data is already downloaded into combined_datasets/
# crisisnlp data: https://drive.google.com/drive/u/0/folders/1-qNFYolOyY01JpsKYLbVSrOGwqaqZhAc
def map_labels(row):
    event_type = row["event_type"]
    if event_type == "fire":
        row["event_type"] = "wildfire"
    return row
crisisnlp = {split: load_dataset("csv", delimiter="\t", data_files=os.path.join(DATA_DIR, combined_datasets, f"combined_{split}.tsv"), split="train").map(map_labels) for split in hf_dataset.keys()}
for name, crisisnlp_dataset in crisisnlp.items():
    # saves train.tsv, dev.tsv, test.tsv into /data/datasets 
    concatenated = concatenate_datasets([crisisnlp_dataset, hf_dataset[name]])
    concatenated.to_csv(os.path.join(DATA_DIR, f"{name}.tsv"), sep="\t")

