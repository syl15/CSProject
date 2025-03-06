'''
CRON job for periodically polling data from bluesky: https://www.youtube.com/watch?v=EgrpfvBc7ks

Activate a local CRON job:
    1. crontab -l: list out all current jobs
    2. crontab -e: open cron job editor to add a new job
    3. enter a new job command 
        ex: */2 * * * * cd /[absolute path to backend directory] && /[absolute path to backend directory]/.venv_backend/bin/python /[absolute path to backend directory]/bluesky_poller.py
            - */2 * * * * specifies how often to run a job
            - everything else specifies the command to be run by the job
                - in thsi case, we want to open the backend directory, use python in the backend venv to run the bluesky_poller script
    4. save the file. If using vim, use ":wq" and press enter


TODO: Make CRON job Heroku friendly
'''

from atproto import Client, client_utils
from dotenv import load_dotenv
from datetime import datetime
import os

# create authenticated bsky session to access API
def authenticate_bsky():
    load_dotenv()

    USERNAME = os.getenv("BSKY_USERNAME")
    APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD")

    client = Client()
    client.login(USERNAME, APP_PASSWORD)
    return client

# search for certain # of posts given keyword
def read_bsky_posts(client, keywords=["hurricane", "flood", "fire", "earthquake"], limit=1):
    with open("bluesky_log.txt", "a") as log_file:
        log_file.write("\nAccessed on " + str(datetime.now()) + "\n")

        for keyword in keywords:
            params = {"q": keyword, "limit": limit}
            posts = client.app.bsky.feed.search_posts(params)

            for post in posts.posts:
                log_entry = (
                    f"==== POST ABOUT {keyword.upper()} ====\n"
                    f"Text: {post.record.text}\n"
                    f"Created At: {post.record.created_at}\n"
                    f"Author: {post.author.handle}\n"
                    f"URI: {post.uri}\n\n"
                )
                log_file.write(log_entry)

# def create_cron_job():
#     load_dotenv()

#     cron = CronTab(os.getenv("CRON_USERNAME"))
#     job = cron.new(command=f'{os.getenv("CRON_PYTHON_PATH")} {os.getenv("CRON_SCRIPT_PATH")}')
    
#     job.minute.every(2)
#     cron.write()

if __name__ == "__main__":
    client = authenticate_bsky()
    read_bsky_posts(client)
    # create_cron_job()