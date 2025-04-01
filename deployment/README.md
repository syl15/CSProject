# Deployment Workflow

## Branches 
- `dev`: used for ongoing development 
- `main`: used for stable, production ready code 

All deployments to Render are triggered from the **main** branch **only**. Thus, you should be pushing and pulling from dev during active feature development. We will only push to main when we are ready to deploy significant changes.

## Services 
- `flask-backend`: automatically deploys when `main` is updated (Render watches `backend/`)
- `fastapi-model`: automatically deploys when `main` is updated (Render watches `model/api/`)

## Live endpoints 
- Flask Base URL: https://flask-backend-hu5x.onrender.com/
- FastAPI Base URL: https://fastapi-model-3vkm.onrender.com/

When using these live endpoints, you won't have to manually run the Flask/FastAPI apps locally! 

## Notes: 
- Build minutes are limited, so we should be conscious when pushing to main. 
  - 750 build/deploy minutes per month per account
  - 512 MB RAM per free service
- Free services sleep after 15 minutes of inactivity and may take a few seconds to restart 
    - This means that the first request to a live endpoint after it "sleeps" may take a little longer to load (cold start). 
    - You should not get any errors like 500 or 404, just a brief delay. 