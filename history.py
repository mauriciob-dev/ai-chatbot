import json

MAX_HISTORY = 20

def load_history(username: str) -> list:
    try:
        with open(f"{username}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON for user {username}.")
        return []

def save_history(data: list, username: str) -> None:
    try:
        with open(f"{username}.json", "w") as file:
            json.dump(data, file, indent=2)
    except IOError as e:
        print(f"Error saving history: {e}")

def trim_history(history: list) -> list:
    if len(history) > MAX_HISTORY:
        return history[-MAX_HISTORY:]
    return history