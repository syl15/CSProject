# Backend 

## Core contents 
  - `app.py`: Entry point for Flask app.
    - Automatically runs the backend server via `flask run`
  - `database.py`: Allows backend to connect and interact with PostgreSQL tables via SQL queries
  - `run_pipeline.py`: Full pipeline that polls for new bluesky posts, classifies and clusters them, and writes results back to the database

## Prerequisites 

### Environnment Variables 
Create a `.env` file with the following keys and contact backend developers for the values:     
DATABASE_URL= \
BSKY_USERNAME= \
BSKY_APP_PASSWORD= \
OPENROUTER_API_KEY= \
FASTAPI_BASE_URL= \
FASTAPI_LOCAL_BASE_URL= 

### Virtual Environment
  - [Activate your venv](#activating-your-venv)
    - TLDR: 
      - `source [venv_name]/bin/activate` to activate venv
      - `deactivate` to deactivate venv
  - [Install dependencies](#installing-new-packages)
    - TLDR:
      - `pip install -r backend/requirements.txt` to install backend required packages
  - Host the server by running `flask run` 

### Activating your venv 

Aside: Should you activate your venv from the root directory?
  - Actually, a lot of sources are mixed over whether this is the best practice and there are many ways to do it, but you can pick a workflow that works for you. 
  - Activating the venv from the root, however, does make the venv accessible to all the project subfolder which means you won't have to reactivate if you're navigating to specific subfolders. 

#### If your project is new: 
  - You will need create a new venv
  - Run `python3 -m venv venv` (using whatever python version you have)
  - This creates a `venv` folder in the root directory

#### Recurring steps (instructions for Mac)
1. Navigate to root directory of the project 
2. To activate, run `source venv/bin/activate` 
3. Install requirements `pip install -r [folderName]/requirements.txt`
    - For example, if I wanted to work in the model folder: 
      - `pip install -r model/requirements.txt`
    - If I wanted to switch to backend work: 
       - `pip install -r backend/requirements.txt`
    - You only need to do this if dependencies have changed since you last worked on the project (e.g. after pulling new changes)
4. To deactivate, run `deactivate`

#### Troubleshooting 

If your current venv is corrupted or has conflicting dependencies, you can try deactivating your venv, deleting the old venv and creating a new one. 

1. `deactivate` (deactivate old venv)  
2. `rm -rf venv`  (removes the venv directory)  
3. `python3 -m venv venv` (creates a new venv)  
4. `pip install -r [folderName]/requirements.txt` (reinstall dependencies)

### Installing new packages 

If you're adding new dependencies, ex. you ran `pip install scikit-learn`,  the current `requirements.txt` won't automatically reflect this change. 

So after installation, freeze the environment to update the list of dependencies by running the following command:

`pip freeze > [folderName]/requirements.txt` 
- Example: `pip freeze > backend/requirements.txt` 

And commit the updated `requirements.txt` to version control so everyone else can download it as well. 

The same goes for if you updated an existing package. Alternatively, you can just add the dependency to `requirements.txt` directly, but this won't add the specific version. 


## Using the Flask API routes 

1. Activate your `venv` and install dependencies \
    `source venv/bin/activate` \
    `pip install -r backend/requirements.txt`
2. Run the Flask app \
    `cd backend` \
    `flask run`
3. View the local endpoint: `http://127.0.0.1:5001`


### Overview of API routes

`GET /disasters`
- This is meant to be an overview of all the disasters in our database. It will have less information than the endpoint for each disaster. 
- This has a few optional parameters you can specify. Check out `app.py` for more documentation 
  - `limit`: how many disasters you want to return
  - `startDate`: start date of the disaster
  - To use a parameter, use the format: 
    - `base_url/disasters?key=value?key=value`, where the parameter name is the `key` 
    - Examples: 
      - `http://127.0.0.1:5001/disasters` (returns all) 
      - `http://127.0.0.1:5001/disasters?limit=2` (returns first two)
      - `http://127.0.0.1:5001/disasters?startDate=2024-01-01` 

`GET /disasters/id` 
- This will contain additional information about each disaster, including posts (currently limited to returning a max of 5)
- No other parameters are available  
- You must specify a valid id to get back a disaster 
- Examples: 
  - `http://127.0.0.1:5001/disasters/23` (returns disaster with disaster_id=23)

`GET /disasters/recent` 
- Returns the most recent disaster, with all the metadata and posts 
- No other parameters are available
