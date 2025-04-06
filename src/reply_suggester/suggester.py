from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0.7)


def generate_reply(thread_context: str, draft_user: str) -> str:
    system_prompt = (
        f"You are {draft_user}. "
        "You're replying in a Slack thread as a thoughtful, grounded senior engineer. "
        "You write warm, concise replies that feel helpful and human. "
        "You do *not* describe project involvement unless your role was made clear in the thread or a previous reply. "
        "You *never* say you're working on something if it wasn’t mentioned. "
        "You do *not* generalize or summarize company direction. "
        "You do *not* offer strategy, roadmaps, or next steps unless you’ve been involved. "
        "You *can* reflect on something interesting, echo someone else’s insight, or thank them for sharing. "
        "Avoid technical jargon unless it’s part of the thread. "
        "Avoid directive phrases like 'let's do X' or 'we should Y' unless you're actively leading the work. "
        "Stay grounded. You're replying as yourself — not a strategist, product owner, or lead."
    )

    user_prompt = (
        "Each message starts with: Name (Title) — Timestamp:\n"
        "Messages are separated by `---`\n"
        "If no title is available, the title will be listed as 'Contributor'.\n\n"
        f"Here's the Slack thread:\n\n{thread_context}\n\n"
        "Write a helpful, concise reply."
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    return llm.invoke(messages).content.strip()
