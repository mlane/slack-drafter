from fastapi import FastAPI, Request
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler

from src.config import SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET
from src.slack.slack_handlers import register_handlers

# Required scopes:
# - channels:history
# - chat:write
# - commands
# - users:read
bolt_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)
register_handlers(bolt_app)

app = FastAPI()
handler = SlackRequestHandler(bolt_app)


@app.post("/slack/events")
async def slack_events(req: Request):
    return await handler.handle(req)
