
import yes_or_no
import save_data
from InquirerPy import inquirer 
def search_menu(current_user):
    while True:
        print("\n--- Search ---")
        search_username = input("Enter username to search (or 'b' to go back): ").strip()
        users = save_data.load_dataa() 
        if search_username.lower() == 'b':
            break
        name2 = []
        for name in users.keys():
            if search_username in name and name not in current_user["blocked"] and name != current_user["username"]:
                name2.append(name)
        if len(name2) == 0 :
            print("user didn't found")
            break
        choice = inquirer.select(
            message = " search result: ",
            choices =name2
        ).execute()
        target=users[choice]
        if current_user["username"] in current_user["following"]:
                print(f"You are already following {target['username']}.")
                if yes_or_no.yes_or_no("Do you want to unfollow? (y/n): "):
                    target["followers"].remove(current_user["username"])
                    current_user["following"].remove(target["username"])
                    print("User unfollowed.")
        else:
                if target["is_private"]:
                    print(f"{target['username']}'s profile is private.")
                    print(f"Followers: {len(target['followers'])} | Following: {len(target['following'])} | Posts: {len(target['posts'])}")
                    if yes_or_no.yes_or_no("Do you want to send a follow request? (y/n): "):
                        target["notifications"].append(f"{current_user['username']} sent you a follow request.")
                        target["follow_requests"].add(current_user["username"])
                        print("Follow request sent.")
                else:
                    print("\n--- Profile Info ---")
                    print(f"Username: {target['username']}")
                    print(f"Full Name: {target['full_name']}")
                    print(f"Bio: {target['bio']}")
                    print(f"Followers: {len(target['followers'])} | Following: {len(target['following'])} | Posts: {len(target['posts'])}")
                    if yes_or_no.yes_or_no("Do you want to follow this user? (y/n): "):
                        target["followers"].add(current_user["username"])
                        current_user["following"].add(target["username"])
                        target["notifications"].append(f"{current_user['username']} started following you.")
                        print("User followed.")

