
import json

def convert_sets(obj):
    if isinstance(obj, dict):
        return {k: convert_sets(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_sets(item) for item in obj]
    elif isinstance(obj, set):
        return list(obj)
    return obj

def save_dataa(users, filepath="data.json"):
    with open(filepath, "w") as f:
        json.dump(convert_sets(users), f, indent=4)

def load_dataa(filepath="data.json"):
    with open(filepath, "r") as f:
        return json.load(f)
