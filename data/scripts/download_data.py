import os 
import gdown 

# Downloads train, test, dev sets from local ../datasets directory (https://drive.google.com/drive/u/5/folders/1_RTvKXflGBOdWWaocSOax5JxPzBIz8n1)
train_id = "1ABaDbbrpJvLR-mVX5KW9vXnRuQNufZuQ"
test_id = "1D0H5ASAat1sDzTuqB9VEJozvwrCKQ04w"
dev_id = "1MEx0KFVDUHaWWfWK4XGc_Ch4zaTmcqsh"

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