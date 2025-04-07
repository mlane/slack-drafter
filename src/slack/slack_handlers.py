from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from src.config import SLACK_ALLOWED_USERS
from src.reply_suggester.suggester import generate_reply
from src.slack.slack_utils import extract_slack_ids, format_timestamp, format_user


def suggest_reply(
    channel_id: str, thread_ts: str, draft_user_id: str, client: WebClient, respond
) -> None:
    try:
        result = client.conversations_replies(channel=channel_id, ts=thread_ts)
        messages = result.get("messages", [])
        if not messages:
            respond("Thread is empty or could not be read.")
            return

        context = "\n---\n".join(
            f"{format_user(message['user'], client)} — {format_timestamp(message['ts'])}:\n{message['text']}"
            for message in messages
            if "user" in message
        )
    except SlackApiError as exception:
        respond(f"Could not fetch thread: {exception}")
        return

    draft_user = format_user(draft_user_id, client).rstrip(":")
    reply = generate_reply(context, draft_user)

    try:
        client.chat_postEphemeral(
            channel=channel_id,
            user=draft_user_id,
            text=f"✍️ *Suggested reply:*\n\n{reply}",
            thread_ts=thread_ts,
        )
    except SlackApiError as exception:
        if exception.response["error"] == "not_in_channel":
            respond(
                "⚠️ The bot isn't a member of this channel. Please invite it with `/invite @slack-drafter` and try again."
            )
        else:
            respond(f"❌ Could not fetch thread: {exception}")
        return


def register_handlers(app):
    @app.command("/draft")
    def handle_suggest(ack, body, client, respond):
        # https://marcuslane.slack.com/archives/CJ9Q9TQAK/p1743892840858149
        ack()

        if body["user_id"] not in SLACK_ALLOWED_USERS:
            print(f"User {body['user_id']} ran /draft on {body.get('text')}")
            respond(
                "Hey! This is still in private testing. You can follow along at https://github.com/mlane/slack-drafter."
            )
            return

        if "archives" not in body.get("text", ""):
            respond(
                "⚠️ That doesn't look like a Slack thread link. Please paste the full URL."
            )
            return

        slack_ids = extract_slack_ids(body.get("text"))

        if not slack_ids:
            respond(
                "Please include a url (e.g. /draft https://marcuslane.slack.com/archives/CJ9Q9TQAK/p1743892840858149)."
            )
            return

        suggest_reply(
            channel_id=slack_ids.get("channel_id"),
            thread_ts=slack_ids.get("thread_ts"),
            draft_user_id=body["user_id"],
            client=client,
            respond=respond,
        )
