import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SLACK_ALLOWED_USERS = set(
    user.strip()
    for user in os.getenv("SLACK_ALLOWED_USERS", "").split(",")
    if user.strip()
)
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
