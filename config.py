from os import getenv
from dotenv import load_dotenv

load_dotenv("info.env")

API_TOKEN = getenv("API_TOKEN", "")
if API_TOKEN == "":
    raise ValueError("API_TOKEN is not set")
