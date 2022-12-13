import json
import os

API_ID: int = int(os.getenv("API_ID"))
API_HASH: str = os.getenv("API_HASH")
BOT_TOKEN: str = os.getenv("BOT_TOKEN")
CHANNEL_ID: int = int(os.getenv("CHANNEL_ID"))



def get_clasifications():
    with open("types.json", "r") as f:
        return json.load(f)


types = get_clasifications()
