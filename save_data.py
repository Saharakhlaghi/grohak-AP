
import json

def save_dataa(users,filepath="data.json"):
    with open(filepath, "w") as f:
        json.dump(users, f, indent=4)
def load_dataa(filepath="data.json"):
    with open(filepath, "r") as f:
        return json.load(f)