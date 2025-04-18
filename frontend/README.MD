# Frontend 

## Core Contents 
- `/components`: all resusable components such as `Map`, `Navbar`, `PieChart`, etc. 
- `/App.jsx`: core React app 

## Prerequisites 

### Environment Variables

Create a `.env` file with the following keys and contact backend developers for the values: \
VITE_BASE_URL= \
VITE_LOCAL_BASE_URL=

## Running the React + Vite app 

1. Install dependencies and run the app: \
`cd frontend` \
`npm install` \
`npm run dev` 
2. To exit the app: \
`q + return` or \
`ctrl + c`


### Testing with live/local URLs

1. Add the .env file to the root `frontend` directory with the two required URLs: 
  - VITE_BASE_URL (live url) 
  - VITE_LOCAL_BASE_URL (localhost url)
2. In `config.js`: 
  - Uncomment out whatever url you want to use. 
3. To use in a file, use the following import: 
  - `import { BASE_URL } from "./config";` 
    - Exact import statement may be different depending on what directory you are in. 