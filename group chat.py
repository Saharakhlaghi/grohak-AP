import json
import os
from datetime import datetime
from InquirerPy import inquirer

GROUPS_FILE = "groups.json"

def load_groups(filepath=GROUPS_FILE):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_groups(groups, filepath=GROUPS_FILE):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=4)

def create_group_chat(current_user, users, groups):
    name = input("Group name: ").strip()
    if not name or name in groups:
        print("Invalid or existing group.")
        return
    choices = [u for u in users if u != current_user["username"]]
    members = inquirer.checkbox(message="Add members:", choices=choices).execute()
    groups[name] = {
        "members": [current_user["username"]] + members,
        "messages": []
    }
    save_groups(groups)
    print(f"Group '{name}' created.")

def join_group_chat(current_user, groups):
    available = [g for g,d in groups.items() if current_user["username"] not in d["members"]]
    if not available:
        print("No groups to join.")
        return
    name = inquirer.select(message="Join which group?", choices=available).execute()
    groups[name]["members"].append(current_user["username"])
    save_groups(groups)
    print(f"You joined '{name}'.")

def leave_group_chat(current_user, groups):
    member_of = [g for g,d in groups.items() if current_user["username"] in d["members"]]
    if not member_of:
        print("You are in no groups.")
        return
    name = inquirer.select(message="Leave which group?", choices=member_of).execute()
    groups[name]["members"].remove(current_user["username"])
    if not groups[name]["members"]:
        del groups[name]
        print(f"Group '{name}' deleted (no members).")
    else:
        print(f"You left '{name}'.")
    save_groups(groups)

def view_group_messages(current_user, groups, name):
    msgs = groups[name]["messages"]
    if not msgs:
        print("No messages.")
    else:
        for sender, text, ts in msgs:
            print(f"[{ts}] {sender}: {text}")
    input("Press Enter to continue...")

def send_group_message(current_user, groups, name):
    text = input("Message: ").strip()
    if not text:
        return
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    groups[name]["messages"].append((current_user["username"], text, ts))
    save_groups(groups)
    print("Message sent.")

def group_chat_session(current_user, users, groups, name):
    while True:
        choice = inquirer.select(
            message=f"=== {name} ===",
            choices=["View Messages", "Send Message", "Add Member", "Remove Member", "Leave Group", "Back"]
        ).execute()
        if choice == "View Messages":
            view_group_messages(current_user, groups, name)
        elif choice == "Send Message":
            send_group_message(current_user, groups, name)
        elif choice == "Add Member":
            avail = [u for u in users if u not in groups[name]["members"]]
            if avail:
                picked = inquirer.checkbox(message="Add:", choices=avail).execute()
                groups[name]["members"].extend(picked)
                save_groups(groups)
        elif choice == "Remove Member":
            rems = [u for u in groups[name]["members"] if u != current_user["username"]]
            if rems:
                picked = inquirer.checkbox(message="Remove:", choices=rems).execute()
                for u in picked:
                    groups[name]["members"].remove(u)
                save_groups(groups)
        elif choice == "Leave Group":
            leave_group_chat(current_user, groups)
            break
        else:
            break

def group_chat_menu(current_user, users):
    groups = load_groups()
    while True:
        choice = inquirer.select(
            message="=== Group Chats ===",
            choices=["Create Group", "Join Group", "Open Group", "Leave Group", "Back"]
        ).execute()
        if choice == "Create Group":
            create_group_chat(current_user, users, groups)
        elif choice == "Join Group":
            join_group_chat(current_user, groups)
        elif choice == "Open Group":
            owned = [g for g,d in groups.items() if current_user["username"] in d["members"]]
            if owned:
                name = inquirer.select(message="Select group:", choices=owned).execute()
                group_chat_session(current_user, users, groups, name)
        elif choice == "Leave Group":
            leave_group_chat(current_user, groups)
        else:
            break
