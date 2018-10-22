from dotenv import load_dotenv, find_dotenv
import os

def load_env():
    print('Loading environment variables.')
    load_dotenv(find_dotenv())
    print('FMI apikey with os.environ: ', os.environ["FMI_API_KEY"])
    print('FMI apikey with os.getenv: ', os.getenv("FMI_API_KEY"))
    