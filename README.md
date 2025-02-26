# CSProject

## How to use the data 

#### Dataset overview: 
I've given everyone access to all datasets obtained from CrisisNLP. You can find the GDrive link [here](https://drive.google.com/drive/folders/1Gmm5frRwloIV6Ur5yoCPjKRJ31UnQ1RY?usp=sharing). 

Here is what each subfolder represents: 
1. `events_set1`
    - Contains many directories, such as `srilanka_floods_2017`, `puebla_mexico_earthquake_2017`, each with a `train.tsv`, `test.tsv`, and `dev.tsv` for events that occured 2016-2017
    - Each `.tsv` contains `tweet_id`, `tweet_text`, and `class_label`
2. `events_set2`
    - Same as `events_set1`, but for events that occured from 2018-2019
3. `event_type`
    - Categorizes data by event types earthquake, fire, flood, and hurricane, each with a `train.tsv`, `test.tsv`, and `dev.tsv`
    - Each `.tsv` contains `tweet_id`, and `class_label`
4. `all_combined` 
    - Combines all data into `train.tsv`, `test.tsv`, and `dev.tsv`
    - Each `.tsv` contains `tweet_id`, and `class_label`
4. `combined_datasets` **
    - The dataset I created by merging `events_set1` and `events_set2` because they contain the actual tweet text and the specific event names. I also manually assigned the `event_type` as a label for classification later on. 
    - This is the dataset we will be focusing on, but I've included the other ones in case they are helpful

#### How to actually get the data in your repository:

To make this easier and for standardization, I've written a python script called `download_data.py` available in the `/data/scripts` directory. This will automatically download `train.tsv`, `test.tsv`, and `dev.tsv` from `combined_datasets` to your local `data` directory. If you would like any of the other datasets, feel free to update the script accordingly. 

To use the script, run:
1. `pip3 install gdown` (globally) 
2. `python3 download_data.py` (after navigating the proper directory). 

Note: exact commands might be different depending on your python and pip version.

You should be able to see the three datasets in your `data` directory. To test whether they work, you can access the `test.ipynb` notebook in the `model/notebooks` directory and run the first cell. 

I've added the `data` directory to `.gitignore` because GitHub can't support such large files. As a result, you'll be working with the data on your local repository. 

### TODO
- Licensing info, especially for Crisis NLP 