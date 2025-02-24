# !pip install datasets
from datasets import load_dataset, concatenate_datasets, Value
import pandas as pd

base_url = "https://huggingface.co/datasets/nlp-pw/Disaster-Tweets-Normalized/resolve/main/data/"
parquet_files = {'train': base_url+'train-00000-of-00001.parquet', 'test': base_url+'test-00000-of-00001.parquet'}

splits = parquet_files.keys()
unwanted_columns = ["hashtags", "emojis", "__index_level_0__"]

hf_dataset = {}
for split in splits:
    hf_dataset[split] = load_dataset('parquet', data_files=parquet_files, split=split).remove_columns(unwanted_columns).rename_column("disaster_type", "event_type").filter(lambda row: row["event_type"] == "unrelated")

test_dev_split = hf_dataset["test"].train_test_split(test_size=0.5)
hf_dataset["test"] = test_dev_split["train"]
hf_dataset["dev"] = test_dev_split["test"]

for a, b in hf_dataset.items():
    hf_dataset[a] = b.add_column(name="class_label", column=("None" for i in range(len(b)))).add_column(name="specific_event_name", column=("None" for i in range(len(b)))).cast_column("tweet_id", Value("int64"))

crisisnlp = {split: load_dataset("csv", delimiter="\t", data_files=f"data/{split}.tsv")["train"] for split in hf_dataset.keys()}
for name, crisisnlp_dataset in crisisnlp.items():
    concatenated = concatenate_datasets([crisisnlp_dataset, hf_dataset[name]])
    concatenated.to_csv(f"all_data/all_{name}.tsv", sep="\t")
