import json
import os
def load_chats():
    if not os.path.exists("chats.json") or os.stat("chats.json").st_size == 0:
        return {}
    with open("chats.json", "r") as f:
        data = json.load(f)
        return {
            tuple(k.split(",")): v  
            for k, v in data.items()
        }

def save_chats(chats):
    json_ready = {
        f"{k[0]},{k[1]}": v
        for k, v in chats.items()
        if isinstance(k, tuple) and len(k) == 2
    }
    with open("chats.json", "w") as f:
        json.dump(json_ready, f, indent=4)
