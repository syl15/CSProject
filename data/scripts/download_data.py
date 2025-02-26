import os 
import gdown 

# Downloads train, test, dev sets from combined_datasets
train_id = "1EQMnszXXJCR47xEK6QA75Wf-lJd5DJJZ"
test_id = "1uIFfYOfoWB2gcOVbQB-CXCdUKaRL-i-2"
dev_id = "1lmxndA9eZLmwvdAqNBpzsMi3_Uf-cNHV"

files_info = [
    {"url": f"https://drive.google.com/uc?id={train_id}", "filename": "train.tsv"}, 
    {"url": f"https://drive.google.com/uc?id={test_id}", "filename": "test.tsv"},
    {"url": f"https://drive.google.com/uc?id={dev_id}", "filename": "dev.tsv"}
]

# Relative path to data directory 
data_directory = "../datasets" 

# If data folder does not exist, create it
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# Download files to the data directory 
for file_info in files_info: 
    url = file_info["url"]
    filename = file_info["filename"]
    print(f"Downloading {url} as {filename}...")
    gdown.download(url, os.path.join(data_directory, filename), quiet=False)

print("Download complete")