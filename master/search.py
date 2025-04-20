import yes_or_no
import save_data
from InquirerPy import inquirer
from Block import *

def search_menu(current_user):
    while True:
        print("\n--- Search ---")
        search_username = input("Enter username to search (or 'b' to go back): ").strip()
        
        users = save_data.load_dataa()  
        current_user = users[current_user["username"]]  

        if search_username.lower() == 'b':
            return

        name2 = []
        for name in users.keys():
            if search_username in name and name not in current_user.get("blocked", []) and current_user["username"] not in users[name].get("blocked", []) and name != current_user["username"]:
                name2.append(name)

        if not name2:
            print("User not found.")
            break

        choice = inquirer.select(
            message="Search result:",
            choices=name2
        ).execute()

        target = users[choice]

        while True:
            actions = []

            if target["username"] in current_user["following"]:
                actions.append("Unfollow")
            elif not target["is_private"]:
                actions.append("Follow")
            else:
                actions.append("Request to Follow")

            if target["username"] in current_user.get("blocked", []):
                actions.append("Unblock")
            else:
                actions.append("Block")

            actions.append("View Profile Info")
            actions.append("Back")

            selected = inquirer.select(
                message=f"What would you like to do with {target['username']}?",
                choices=actions
            ).execute()

            if selected == "Unfollow":
                if current_user["username"] in target.get("followers", []):
                    target["followers"].remove(current_user["username"])
                if target["username"] in current_user.get("following", []):
                    current_user["following"].remove(target["username"])
                print("User unfollowed.")
                save_data.save_dataa(users)

            elif selected == "Follow":
                if current_user["username"] not in target["followers"]:
                    target["followers"].append(current_user["username"])
                if target["username"] not in current_user["following"]:
                    current_user["following"].append(target["username"])
                target.setdefault("notifications", []).append(f"{current_user['username']} started following you.")
                print("User followed.")
                save_data.save_dataa(users)

            elif selected == "Request to Follow":
                print(f"{target['username']}'s profile is private.")
                print(f"Followers: {len(target['followers'])} | Following: {len(target['following'])} | Posts: {len(target['posts'])}")
                if yes_or_no.yes_or_no("Send follow request? (y/n): "):
                    if not current_user["username"] in target["follow_requests"]:
                        target.setdefault("follow_requests", set()).append(current_user["username"])
                        target.setdefault("notifications", []).append(f"{current_user['username']} sent you a follow request.")
                        print("Follow request sent.")
                        save_data.save_dataa(users)
                    else:
                        print("you already sent a request")

            elif selected == "Block":
                current_user.setdefault("blocked", [])
                if target["username"] not in current_user["blocked"]:
                    current_user["blocked"].append(target["username"])
                    if target["username"] in current_user["following"]:
                        current_user["following"].remove(target["username"])
                    if current_user["username"] in target["followers"]:
                        target["followers"].remove(current_user["username"])
                    target.setdefault("notifications", []).append(f"You were blocked by {current_user['username']}.")
                    print(f"Blocked {target['username']}")
                    save_data.save_dataa(users)

            elif selected == "Unblock":
                if target["username"] in current_user.get("blocked", []):
                    current_user["blocked"].remove(target["username"])
                    target.setdefault("notifications", []).append(f"You were unblocked by {current_user['username']}.")
                    print(f"Unblocked {target['username']}")
                    save_data.save_dataa(users)

            elif selected == "View Profile Info":
                print("\n--- Profile Info ---")
                print(f"Username: {target['username']}")
                print(f"Full Name: {target['full_name']}")
                print(f"Bio: {target['bio']}")
                print(f"Followers: {len(target['followers'])} | Following: {len(target['following'])} | Posts: {len(target['posts'])}")
                input("Press Enter to continue...")

            elif selected == "Back":
                break
