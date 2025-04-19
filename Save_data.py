import json

def save_chats(chats):
    with open("chats.json", "w") as f:
        json.dump(chats, f)




def load_chats():
    try:
        with open("chats.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
