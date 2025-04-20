from InquirerPy import inquirer
import save_data

def block_user(current_user, users):
    available = [u for u in users if u != current_user["username"] and u not in current_user.get("blocked", [])]
    if not available:
        print("No users available to block.")
        return
    to_block = inquirer.select(
        message="Select a user to block:",
        choices=available
    ).execute()
    
    current_user.setdefault("blocked", [])
    current_user["blocked"].append(to_block)

    if to_block in current_user.get("followers", []):
        current_user["followers"].remove(to_block)
    if to_block in current_user.get("following", []):
        current_user["following"].remove(to_block)

    users[to_block].setdefault("notifications", []).append(
        f"You were blocked by {current_user['username']}.")
    save_data.save_dataa(users)
    print(f"User '{to_block}' has been blocked.")


def unblock_user(current_user, users):
    blocked = current_user.get("blocked", [])
    if not blocked:
        print("You have no blocked users.")
        return
    to_unblock = inquirer.select(
        message="Select a user to unblock:",
        choices=blocked
    ).execute()
    current_user["blocked"].remove(to_unblock)
    users[to_unblock].setdefault("notifications", []).append(
        f"You were unblocked by {current_user['username']}.")
    save_data.save_dataa(users)
    print(f"User '{to_unblock}' has been unblocked.")


def block_menu(current_user, users):
    while True:
        choice = inquirer.select(
            message="=== Block / Unblock ===",
            choices=["Block User", "Unblock User", "Back"]
        ).execute()
        if choice == "Block User":
            block_user(current_user, users)
        elif choice == "Unblock User":
            unblock_user(current_user, users)
        else:
            break
