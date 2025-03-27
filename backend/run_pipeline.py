'''
CRON job for periodically polling/processig data: https://www.youtube.com/watch?v=EgrpfvBc7ks

Activate a local CRON job:
    1. crontab -l: list out all current jobs
    2. crontab -e: open cron job editor to add a new job
    3. enter a new job command 
        ex: */2 * * * * cd /[absolute path to backend directory] && /[absolute path to backend directory]/.venv_backend/bin/python /[absolute path to backend directory]/bluesky_poller.py
            - */2 * * * * specifies how often to run a job
            - everything else specifies the command to be run by the job
                - in this case, we want to open the backend directory and use python from the backend venv to run the bluesky_poller script
    4. save the file. If using vim, use ":wq" and press enter


TODO: Make CRON job Heroku friendly
'''

from bluesky_poller import poll_bsky_posts, authenticate_bsky
from bluesky_processor import process_bluesky_data

def run_pipeline():
    client = authenticate_bsky()
    poll_bsky_posts(client, limit=1)
    process_bluesky_data()

    print("✅ Pipeline complete.")

if __name__ == "__main__":
    run_pipeline()