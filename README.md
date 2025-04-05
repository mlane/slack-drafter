# slack-reply-assistant

A lightweight, GPT-powered Slack bot that suggests thoughtful, personalized replies whenever you're mentioned in a thread.

> Inspired by the [LLM Engineering Cheatsheet](https://github.com/mlane/llm-engineering-cheatsheet)

- ✨ Automatically triggers when you're mentioned
- 🧵 Understands thread context to avoid repeating what's already been said
- 🧑‍💼 Adapts to your tone (IC vs leader)
- 👀 Review-first: Suggestions are private until you click to send
- ⚡ Built with FastAPI, OpenAI, and Slack Bolt

> Perfect for engineers, PMs, and creators who want to reply faster — without losing their voice.

---

## Quickstart

```bash
git clone https://github.com/mlane/slack-reply-assistant.git
cd slack-reply-assistant

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.sample .env
# Then add your OpenAI + Slack credentials

# Run locally (uses FastAPI + Slack events)
python src/main.py
```

---

## 🔑 .env Setup

Copy the `.env.sample` and fill in:

```
OPENAI_API_KEY=your-openai-key
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_APP_TOKEN=xapp-your-slack-app-level-token
SLACK_USER_ID=U12345678  # Your Slack user ID to detect mentions
```

> Tip: You can find your Slack user ID by clicking on your name in Slack → More → Copy member ID

---

## Personalization

To customize replies to your voice:

1. Add 3–5 example Slack replies you’ve written to `src/reply_suggester/prompt_builder.py`
2. These will be used as few-shot examples when GPT suggests responses
3. (Optional) Add tone logic to vary replies for ICs vs execs

---

## Slack App Setup

1. Create a Slack App at https://api.slack.com/apps
2. Enable **Socket Mode** and set up **Event Subscriptions**
3. Add these scopes:
   - `channels:history`
   - `chat:write`
   - `commands`
   - `im:history`
   - `users:read`
4. Subscribe to:
   - `app_mention`
   - `message.channels`
5. Install to your workspace and copy the tokens into `.env`

---

## Linting & Format

```bash
# One-time setup
pre-commit install

# Manually run format + lint
black .
ruff check .
```

---

## Deployment

You can deploy to any Python-friendly service like:

- [Fly.io](https://fly.io/)
- [Render](https://render.com/)
- [Railway](https://railway.app/)

Or keep it running on a private always-on server.

---

## Roadmap

- [ ] Ephemeral message suggestions (MVP)
- [ ] Adaptive tone (IC vs leader)
- [ ] App Home tab fallback
- [ ] Add memory/personal context for long-term tone
- [ ] Message quality scoring (e.g., “Too wordy”)

---

## License

[MIT](./LICENSE)

## Feedback

PRs welcome. Please keep things clean, consistent, and low-dependency.
