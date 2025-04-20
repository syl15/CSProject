import os 
import gdown 

# Downloads crisisnlp train, test, dev sets from google drive (https://drive.google.com/drive/folders/1Gmm5frRwloIV6Ur5yoCPjKRJ31UnQ1RY) to local datasets/combined_datasets directory
train_id = "1051g1Y5xUc716CR5bqeaVYH0D-cFnm5I"
test_id = "100ck2eOW37Sg7o6SFu_rqwM6XnQnYosA"
dev_id = "1-sXOLEh10vnIa_FgVWOCOqBmC37acpMu"

files_info = [
    {"url": f"https://drive.google.com/uc?id={train_id}", "filename": "train.tsv"}, 
    {"url": f"https://drive.google.com/uc?id={test_id}", "filename": "test.tsv"},
    {"url": f"https://drive.google.com/uc?id={dev_id}", "filename": "dev.tsv"}
]

# Relative path to data directory 
data_directory = "../datasets/combined_datasets" 

# If data folder does not exist, create it
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# Download files to the data directory 
for file_info in files_info: 
    url = file_info["url"]
    filename = file_info["filename"]
    print(f"Downloading {url} as {filename}...")
    gdown.download(url, os.path.join(data_directory, f"combined_{filename}"), quiet=False)

print("Download complete")