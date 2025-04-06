import re
from datetime import datetime
from urllib.parse import parse_qs, urlparse

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from src.reply_suggester.suggester import generate_reply


def extract_slack_ids(url: str):
    if not url:
        return {}

    # Parse the URL
    parsed = urlparse(url)
    path = parsed.path
    query = parse_qs(parsed.query)

    # Regex to extract from path
    match = re.search(r"/archives/([A-Z0-9]+)/p(\d{10})(\d{6})", path)
    if match:
        channel_id = match.group(1)
        ts_seconds = match.group(2)
        ts_micro = match.group(3)
        thread_ts = f"{ts_seconds}.{ts_micro}"
        return {"channel_id": channel_id, "thread_ts": thread_ts}

    # Fallback: try to extract from query params (some shared links use ?thread_ts=...)
    match = re.search(r"/archives/([A-Z0-9]+)", path)
    if match and "thread_ts" in query:
        return {"channel_id": match.group(1), "thread_ts": query["thread_ts"][0]}

    raise ValueError("Could not extract channel/thread ID from Slack URL.")


def format_timestamp(ts: str) -> str:
    dt = datetime.fromtimestamp(float(ts))
    return dt.strftime("%Y-%m-%d %I:%M %p")


def format_user(user_id: str, client: WebClient) -> str:
    try:
        user_info = client.users_info(user=user_id)
        profile = user_info.get("user", {}).get("profile", {})

        display_name = profile.get("display_name")
        first_name = profile.get("first_name")
        last_name = profile.get("last_name")
        title = profile.get("title") or "Contributor"  # fallback here

        name = (
            f"{first_name} {last_name}".strip()
            if first_name and last_name
            else display_name or first_name or user_id
        )

        return f"{name} ({title}):"
    except Exception as exception:
        print(f"Error formatting user {user_id}: {exception}")
        return user_id


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
    except SlackApiError:
        respond("❌ Failed to post suggestion.")


def register_handlers(app):
    @app.command("/draft")
    def handle_suggest(ack, body, client, respond):
        # https://marcuslane.slack.com/archives/CJ9Q9TQAK/p1743892840858149
        ack()

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
