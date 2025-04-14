### Running the React app
cd frontend \
npm install \
npm run dev 

To exit: \
q + return

### Testing with live/local URLs

1. Add a .env file to the root `frontend` directory
2. Add the two URLs
  - VITE_BASE_URL (live url) 
  - VITE_LOCAL_BASE_URL (localhost url)
3. In `config.js`: 
  - Comment out whatever url you want to use. 
4. To use in a file, use the following import: 
  - `import { BASE_URL } from "./config";` 
    - Exact import statement may be different depending on what directory you are in. 