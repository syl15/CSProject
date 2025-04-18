# Deployment 

## Workflow and branches 
- `dev`: used for ongoing development 
- `main`: used for stable, production ready code 

All deployments to Render are triggered from the **main** branch **only**. Thus, you should be pushing and pulling from dev during active feature development. We will only push to main when we are ready to deploy significant changes.

## Services 
- `flask-backend`: automatically deploys when `main` is updated (Render watches `backend/`)
- `fastapi-model`: automatically deploys when `main` is updated (Render watches `model/api/`)

## Live endpoints 
- Flask Base URL: [ASK BACKEND TEAM]
- FastAPI Base URL: [ASK  BACKEND TEAM]

When using these live endpoints, you won't have to manually run the Flask/FastAPI apps locally! 

## Notes: 
- Build minutes are limited, so we should be conscious when pushing to main. 
  - 750 build/deploy minutes per month per account
  - 512 MB RAM per free service
- Free services sleep after 15 minutes of inactivity and may take a few seconds to restart 
    - This means that the first request to a live endpoint after it "sleeps" may take a little longer to load (cold start). 
    - You should not get any errors like 500 or 404, just a brief delay. 
- The free plan of Render does not allow multiple collaborators on a single project, so there is no way for multiple people to deploy to the same hosted urls. 
  - However, you are free to run your own deployment if you wish. 
  - You can set up a Render account and use the `render.yaml` file in the root directory for a ["Blueprint Deploy".](https://render.com/docs/infrastructure-as-code) 
    - This will deploy the services with your own account. I'd recommend this if you just want to try out deploying, but it's not really necessary. It will also deploy your services to their own urls, not the shared live ones.
  - The way we can collaborate together is that everyone will push to dev, I can merge to main and handle the deployment from there.  