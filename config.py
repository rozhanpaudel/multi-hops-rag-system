from dotenv import load_dotenv
import os

load_dotenv() 


def get_environment_config(key):
    return os.environ[key]
