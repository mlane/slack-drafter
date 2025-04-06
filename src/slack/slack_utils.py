import re
from datetime import UTC, datetime
from urllib.parse import parse_qs, urlparse

from slack_sdk import WebClient


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
    dt = datetime.fromtimestamp(float(ts), tz=UTC)
    return dt.strftime("%Y-%m-%d %I:%M %p UTC")


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
