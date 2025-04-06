import pytest

from src.slack.slack_utils import extract_slack_ids, format_timestamp


def test_extract_slack_ids_invalid_url():
    url = "https://workspace.slack.com/messages/general"
    with pytest.raises(ValueError):
        extract_slack_ids(url)


def test_extract_slack_ids_query_params():
    url = "https://workspace.slack.com/archives/C98765432?thread_ts=1714774008.000000"
    ids = extract_slack_ids(url)
    assert ids["channel_id"] == "C98765432"
    assert ids["thread_ts"] == "1714774008.000000"


def test_extract_slack_ids_valid_url():
    url = "https://workspace.slack.com/archives/C12345678/p1714774008000000"
    ids = extract_slack_ids(url)
    assert ids["channel_id"] == "C12345678"
    assert ids["thread_ts"] == "1714774008.000000"


def test_format_timestamp():
    ts = "1714774008.000000"
    formatted = format_timestamp(ts)
    assert formatted == "2024-05-03 10:06 PM UTC"
