import os
from dotenv import load_dotenv

load_dotenv()

BROKER_NAME = os.getenv("BROKER_NAME")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
