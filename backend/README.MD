### Contents of this folder
  - Items you need to create:
    1. `.env`:
      - Stores DB URL, bluesky credentials, openrouter API key, fastAPI live link, and fastAPI local link
      - Contact backend developer for this info
  - `app.py`: Entry point for Flask app.
  - `database.py`: Allows backend to connect and interact with PostgreSQL tables via SQL queries
  - `run_pipeline.py`: Pulls, processes, and clusters data periodically.

### Using the Flask API routes 

1. Activate your `venv` and install dependencies
    `source venv/bin/activate` \
    `pip install -r backend/requirements.txt`
2. Run the Flask app \
    `cd backend` \
    `flask run`
3. Run the React app \
    `cd frontend` \
    `npm install` \
    `npm run dev`

You should be able to see the API responses on `http://localhost:5173/`.

### Overivew of API routes

`GET /disasters`
- This is meant to be an overview of all the disasters in our database. It will have less information than the endpoint for each disaster. 
- This has a few optional parameters you can specify. Check out `app.py` for more documentation 
  - limit (how many disasters you want to return)
  - startDate (start date of the disaster)
  - To use a parameter, use the format: 
    - `base_url/disasters?key=value?key=value`, where the parameter name is the `key` 
    - Examples: 
      - `http://127.0.0.1:5001/disasters` (returns all) 
      - `http://127.0.0.1:5001/disasters?limit=2` (returns first two)
      - `http://127.0.0.1:5001/disasters?startDate=2024-01-01` 

`GET /disasters/id` 
- This will contain additional information about each disaster, including posts (currently limited to returning a max of 10)
- No other parameters are available  
- You must specify a valid id to get back a disaster 
- Examples: 
  - `http://127.0.0.1:5001/disasters/23` (returns disaster with disaster_id=23)

`GET /disasters/recent` 
- Returns the most recent disaster, with all the metadata and posts 
- No other parameters are available
