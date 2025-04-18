def get_chat_key(user1, user2):
    return tuple(sorted([user1, user2]))

def view_messages(current_user):
    while True:
        print(" Messages ")   
        user_chats = [key for key in chats if current_user["username"] in key]
        options = []
        chat_lookup = {}

        if user_chats:
            for chat_key in user_chats:
                other = [uname for uname in chat_key if uname != current_user["username"]][0]
                label = f"Chat with {other}"
                options.append(label)
                chat_lookup[label] = other
        else:
            print("No chats available.")

        options.extend(["Start a new chat", "Back"])
        choice = inquirer.select(
            message="",
            choices=options,
        ).execute()

        if choice == "Start a new chat":
            available_users = [
                uname for uname in users
                if uname != current_user["username"]
                and uname not in current_user["blocked"]
            ]

            if not available_users:
                print("No available users to chat with.")
                continue

            target_username = inquirer.select(
                message="Choose a user to chat with:",
                choices=available_users
            ).execute()

            chat_key = get_chat_key(current_user["username"], target_username)
            if chat_key not in chats:
                chats[chat_key] = []

            chat_session(current_user, target_username, chat_key)

        elif choice == "Back":
            break

        else:
            target_username = chat_lookup[choice]
            chat_key = get_chat_key(current_user["username"], target_username)
            chat_session(current_user, target_username, chat_key)


def chat_session(current_user, target_username, chat_key):
    while True:
        print(f"\n   Chat with {target_username}")
        messages = chats.get(chat_key, [])
        if messages:
            for sender, message in messages:
                display_name = "you" if sender == current_user["username"] else sender
                print(f"{display_name}: {message}")
        else:
            print("No messages.")

        choice = inquirer.select(
            message="",
            choices=[
                "Write a new message",
                "Back"
            ]
        ).execute()

        if choice == "Write a new message":
            msg = inquirer.text(message="Your message:").execute().strip()
            if msg:
                chats[chat_key].append((current_user["username"], msg))
                users[target_username]["notifications"].append(
                    f"New message from {current_user['username']}."
                )
                print("Message sent.")

        elif choice == "Back":
            break