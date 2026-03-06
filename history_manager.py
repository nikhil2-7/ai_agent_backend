import json
import os

HISTORY_FILE = "chat_history.json"
MAX_HISTORY = 7


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def add_conversation(human_message, ai_message):
    history = load_history()

    # 🔥 Insert new conversation at TOP
    history.insert(0, {
        "human": human_message,
        "ai": ai_message
    })

    # 🔥 Keep only latest 7 conversations
    history = history[:MAX_HISTORY]

    save_history(history)