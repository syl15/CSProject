### Activiating your venv 

Aside: Should you activate your venv from the root directory?
  - Actually, a lot of sources are mixed over whether this is the best practice and there are many ways to do it, but you can pick a workflow that works for you. 
  - Activating the venv from the root, however, does make the venv accessible to all the project subfolder which means you won't have to reactivate if you're navigating to specific subfolders. 

If your project is new: 
  - You will need create a new venv
  - Run `python3 -m venv venv` (using whatever python version you have)
  - This creates a `venv` folder in the root directory

Recurring steps (instructions for Mac)
1. Navigate to root directory of the project 
2. To activate, run `source venv/bin/activate` 
3. Install requirements `pip install -r [folderName]/requirements.txt`
    - For example, if I wanted to work in the model folder: 
      - `pip install -r model/requirements.txt`
    - If I wanted to switch to backend work: 
       - `pip install -r backend/requirements.txt`
    - You only need to do this if dependencies have changed since you last worked on the project (e.g. after pulling new changes)
4. To deactivate, run `deactivate`


If your current venv is corrupted or has conflicting dependencies, you can try deactivating your venv, deleting the old venv and creating a new one. 

`deactivate` (deactivate old venv)  
`rm -rf venv`  (removes the venv directory)  
`python3 -m venv venv` (creates a new venv)  
`pip install -r [folderName]/requirements.txt` (reinstall dependencies)

### Installing new packages 

If you're adding new dependencies, ex. you ran `pip install scikit-learn`,  the current `requirements.txt` won't automatically reflect this change. 

So after installation, freeze the environment to update the list of dependencies by running the following command:

`pip freeze > [folderName]/requirements.txt` 

  Example: `pip freeze > backend/requirements.txt` 

And commit the updated requirements to version control. 

The same goes for if you updated an existing package. 