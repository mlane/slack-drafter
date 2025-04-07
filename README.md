# slack-drafter

A lightweight GPT-powered **Slack bot** that helps you reply faster — without sounding like a robot.

> Powered by GPT-4 + LangChain. Designed for thoughtful humans who want to save time.

---

## Features

- ⌨️ Use `/draft [thread URL]` in Slack to generate a reply suggestion
- 🧵 Understands full thread context to avoid repetition
- 🔣 Adapts to your voice (IC-focused tone by default)
- 🔒 Replies are private until you choose to send them
- ⚡ Built with FastAPI, Slack Bolt, and LangChain

---

## Quickstart

```bash
git clone https://github.com/mlane/slack-drafter.git
cd slack-drafter

# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit environment variables
cp .env.sample .env
# Then add your OpenAI and Slack credentials
```

Run the app:

```bash
python src/main.py
```

---

## Environment Variables

```env
LANGCHAIN_API_KEY=your-langchain-api-key
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_PROJECT=your-project-name
LANGCHAIN_TRACING_V2=true
OPENAI_API_KEY=your-openai-key
SLACK_APP_TOKEN=xapp-your-slack-token
SLACK_BOT_TOKEN=xoxb-your-slack-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_USER_ID=your-slack-user-id
```

---

## Minimal Testing

To keep LLM costs low, we recommend basic tests for:

- `extract_slack_ids()`
- `format_timestamp()`
- `format_user()`

Example:

```python
# tests/slack_utils_tests.py
def test_format_timestamp():
    ts = "1714774008.000000"
    formatted = format_timestamp(ts)
    assert formatted == "2024-05-03 10:06 PM UTC"
```

---

## Slack App Setup

1. Create a Slack App at https://api.slack.com/apps
2. Enable **Slash Commands** and **Event Subscriptions**
3. Add these OAuth scopes:
   - `commands`
   - `chat:write`
   - `channels:history`
   - `users:read`
4. Create a slash command:
   - Command: `/draft`
   - Request URL: `https://<your-domain>/slack/events`
5. Install to your workspace

---

## Roadmap

- [x] Slash command reply suggester
- [x] Ephemeral message previews
- [x] Tone tuned to IC voice
- [ ] Optional App Home fallback UI
- [ ] Long-term personalization via memory/context
- [ ] Message quality scoring (e.g., “Too wordy”)

---

## 🧑‍💻 License

[MIT](./LICENSE)

## Contributions

PRs welcome. Please keep things minimal, tested, and low-dependency.

---

## Why "slack-drafter"?

The goal is simple: help you draft thoughtful replies — fast. Whether you're in back-to-back meetings or catching up on threads, this Slack bot gives you a head start without losing your voice.

Previously named `slack-reply-assistant`.
