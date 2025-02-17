import os 
import gdown 

# Downloads train, test, dev sets from combined_datasets
files_info = [
    {"url": "https://drive.google.com/uc?id=1051g1Y5xUc716CR5bqeaVYH0D-cFnm5I", "filename": "train.tsv"}, 
    {"url": "https://drive.google.com/uc?id=1-sXOLEh10vnIa_FgVWOCOqBmC37acpMu", "filename": "dev.tsv"}, 
    {"url": "https://drive.google.com/uc?id=100ck2eOW37Sg7o6SFu_rqwM6XnQnYosA", "filename": "test.tsv"}
]

# Relative path to data directory 
data_directory = "data" 

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