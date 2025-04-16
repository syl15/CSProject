from dotenv import load_dotenv
import os

load_dotenv()

def get_deployed_fastapi_link():
     return os.getenv('FASTAPI_BASE_URL')

def get_local_fastapi_link():
    return os.getenv('FASTAPI_LOCAL_BASE_URL')