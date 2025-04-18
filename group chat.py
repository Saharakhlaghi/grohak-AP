import json
import os
from datetime import datetime
from InquirerPy import inquirer

# File: group_chats.py
# Handles creation and interaction of group chats.

GROUPS_FILE = "groups.json"

def load_groups(filepath=GROUPS_FILE):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

def save_groups(groups, filepath=GROUPS_FILE):
    with open(filepath, "w") as f:
        json.dump(groups, f, indent=4)

# Initialize groups data
groups = load_groups()

def view_group_chats(current_user, users):
    """Main menu for group chats."""
    global groups
    while True:
        # List groups the user is a member of
        user_groups = [name for name, g in groups.items() if current_user["username"] in g["members"]]
        choices = [{"name": f"{name} ({len(groups[name]['members'])} members)", "value": name} for name in user_groups]
        choices.append({"name": "Create New Group", "value": "__create"})
        choices.append({"name": "Back", "value": "__back"})
        
        selection = inquirer.select(
            message="=== Group Chats ===",
            choices=choices
        ).execute()
        
        if selection == "__create":
            create_group(current_user, users)
        elif selection == "__back":
            break
        else:
            view_group_chat(current_user, users, selection)


def create_group(current_user, users):
    """Create a new group with selected members."""
    global groups
    group_name = input("Enter a name for the group: ").strip()
    if not group_name:
        print("Group name cannot be empty.")
        return
    if group_name in groups:
        print("A group with this name already exists.")
        return
    available_users = [u for u in users if u != current_user["username"]]
    if not available_users:
        print("No users available to add.")
        return
    selected = inquirer.checkbox(
        message="Select users to add:",
        choices=available_users
    ).execute()
    members = [current_user["username"]] + selected
    groups[group_name] = {"members": members, "messages": []}
    save_groups(groups)
    print(f"Group '{group_name}' created with members: {', '.join(members)}.")


def view_group_chat(current_user, users, group_name):
    """View and interact within a specific group chat."""
    global groups
    group = groups.get(group_name)
    if not group:
        print("Group not found.")
        return
    while True:
        print(f"\n=== Group: {group_name} ===")
        print("Members:", ", ".join(group["members"]))
        print("\nMessages:")
        for sender, message, timestamp in group["messages"]:
            print(f"[{timestamp}] {sender}: {message}")
        choice = inquirer.select(
            message="Options:",
            choices=["Write Message", "Add Member", "Remove Member", "Back"]
        ).execute()
        
        if choice == "Write Message":
            msg = inquirer.text(message="Your message:").execute().strip()
            if msg:
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                group["messages"].append((current_user["username"], msg, ts))
                save_groups(groups)
                # Notify other members
                for member in group["members"]:
                    if member != current_user["username"]:
                        users[member]["notifications"].append(
                            f"New message in group '{group_name}' from {current_user['username']}."
                        )
                print("Message sent.")
        elif choice == "Add Member":
            available = [u for u in users if u not in group["members"]]
            if not available:
                print("No users to add.")
            else:
                selected = inquirer.checkbox(
                    message="Select users to add:",
                    choices=available
                ).execute()
                for u in selected:
                    group["members"].append(u)
                    users[u]["notifications"].append(
                        f"You were added to group '{group_name}'."
                    )
                save_groups(groups)
        elif choice == "Remove Member":
            removable = [u for u in group["members"] if u != current_user["username"]]
            if not removable:
                print("No members to remove.")
            else:
                selected = inquirer.checkbox(
                    message="Select members to remove:",
                    choices=removable
                ).execute()
                for u in selected:
                    group["members"].remove(u)
                    users[u]["notifications"].append(
                        f"You were removed from group '{group_name}'."
                    )
                save_groups(groups)
        elif choice == "Back":
            break
