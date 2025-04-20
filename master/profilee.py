from InquirerPy import inquirer
from InquirerPy.separator import Separator
from datetime import datetime
import yes_or_no
from save_data import *
import sign_up
import search
from Block import unblock_user

users =load_dataa() 

current_user = {
    "username": " ",
    "password": " ",
    "bio": " ",
    "followers": [],
    "following": [],
    "posts": []
}

other_accounts = {
    "username1": " ",
    "username2": " "
}

def profile_menu(current_user):
    while True:
        choice = inquirer.select(
            message="--- Your Profile ---",
            choices=[
                "View Info and Posts",
                "Add a Post",
                "Add a Story",
                "View Followers/Following",
                "Blocked Users",
                "Update Profile (Name, Bio, Password)",
                "Settings",
                "Delete Account",
                "Back",
            ]
        ).execute()

        if choice == "View Info and Posts":
            print("\n--- Profile Info ---")
            print(f"Username: {current_user['username']}")
            print(f"Full Name: {current_user['full_name']}")
            print(f"Bio: {current_user['bio']}")
            print(f"Profile Type: {'Private' if current_user['is_private'] else 'Public'}")
            print(f"Posts: {len(current_user['posts'])}")

            if current_user["posts"]:
                for idx, post in enumerate(current_user["posts"]):
                    if isinstance(post, str):
                        post = {
                            "content": post,
                            "likes": 0,
                            "comments": [],
                            "shares": 0,
                            "saves": 0,
                            "time": post_time
                        }

                    print(f"{idx + 1}. {post['content']}")
                    print(f"    Likes: {post['likes']} | Comments: {len(post['comments'])} | Shares: {post['shares']} | Saved: {post['saves']} | Time: {post['time']}")
            else:
                print("No posts available.")

            input("Press Enter to go back...")

        elif choice == "Add a Post":
            users = load_dataa()
            content = inquirer.text(message="Enter post content:").execute().strip()
            post_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if content:
                new_post = {
                    "content": content,
                    "time": post_time,
                    "likes": 0,
                    "liked_by": [],
                    "comments": [],
                    "shares": 0,
                    "saves": 0
                }
                current_user["posts"].append(new_post)
                users[current_user["username"]] = current_user

                print("Post added.")
                save_dataa(users)
            else:
                print("Post cannot be empty.")

        elif choice == "Add a Story":
            users = load_dataa()
            story_content = inquirer.text(message="Enter story content:").execute().strip()
            story_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            if story_content:
                new_story = {
                    "content": story_content,
                    "time": story_time,
                    "likes": 0,
                    "liked_by": []
                }
                current_user["stories"].append(new_story)
                users[current_user["username"]] = current_user
                save_dataa(users)

                print("Story added.")
            else:
                print("Story cannot be empty.")
                


        elif choice == "View Followers/Following":
            print("\n--- Followers ---")
            print(", ".join(current_user["followers"]) if current_user["followers"] else "No followers.")

            print("\n--- Following ---")
            following_list = current_user["following"]
            print(", ".join(following_list) if following_list else "Not following anyone.")

            if following_list:
                users = load_dataa()
                do_unfollow = inquirer.confirm(message="Do you want to unfollow someone?", default=False).execute()
                if do_unfollow:
                    to_unfollow = inquirer.select(
                        message="Select a user to unfollow:",
                        choices=following_list
                    ).execute()

                    current_user["following"].remove(to_unfollow)

                    if current_user["username"] in users[to_unfollow]["followers"]:
                        users[to_unfollow]["followers"].remove(current_user["username"])

                    users[to_unfollow].setdefault("notifications", []).append(
                        f"{current_user['username']} unfollowed you.")

                    users[current_user["username"]] = current_user
                    save_dataa(users)

                    print(f"You have unfollowed '{to_unfollow}'.")

            input("Press Enter to go back...")

            
        elif choice == "Blocked Users":
            blocked_users(current_user)
            users[current_user["username"]] = current_user
            save_dataa(users)


        elif choice == "Update Profile (Name, Bio, Password)":
            update_profile(current_user)
            users[current_user["username"]] = current_user
            save_dataa(users)


        elif choice == "Settings":
            profile_settings(current_user)
            users[current_user["username"]] = current_user
            save_dataa(users)


        elif choice == "Delete Account":
            confirm = inquirer.confirm(message="Are you sure you want to delete your account?").execute()
            if confirm:
                users = load_dataa()
                username = current_user["username"]

                for user_data in users.values():
                    if username in user_data.get("followers", []):
                        user_data["followers"].remove(username)
                    if username in user_data.get("following", []):
                        user_data["following"].remove(username)
                    if "notifications" in user_data:
                        user_data["notifications"] = [
                            note for note in user_data["notifications"]
                            if username not in note
                        ]

                users.pop(username, None)

                save_dataa(users)
                print("Account deleted.")
                exit(1)

        elif choice == "Back":
            break


def update_profile(current_user):
    print("\n--- Update Profile ---")
    new_full_name = input("Enter new full name (leave blank to keep current): ").strip()
    new_bio = input("Enter new bio (leave blank to keep current): ").strip()
    new_password = input("Enter new password (leave blank to keep current): ").strip()
    if new_full_name:
        current_user["full_name"] = new_full_name
    if new_bio:
        current_user["bio"] = new_bio
    if new_password:
        current_user["password"] = new_password
    print("Profile updated.")
    

def profile_settings(current_user):
    while True:
        choice = inquirer.select(
            message="--- Settings ---",
            choices=[
                "Saved Posts",
                "Privacy Settings",
                "Back"
            ]
        ).execute()

        if choice == "Saved Posts":
            view_saved_posts(current_user)
        elif choice == "Privacy Settings":
            new_privacy = inquirer.confirm(
                message="Make profile private?",
                default=current_user.get("is_private", False)
            ).execute()
            current_user["is_private"] = new_privacy
            print("Privacy settings updated.")
            save_dataa(users)
        elif choice == "Back":
            break
        save_dataa(users)

def view_saved_posts(current_user):
    print("\n--- Saved Posts ---")
    if not current_user["saved_posts"]:
        print("No saved posts.")
    else:
        for idx, post in enumerate(current_user["saved_posts"]):
            print(f"{idx+1}. {post['content']}")
            print(f"    Likes: {post['likes']} | Comments: {len(post['comments'])} | Shares: {post['shares']} | Saved: {post['saves']}")
    input("Press Enter to go back...")


def blocked_users(current_user):
    print("\n--- Blocked Users ---")
    blocked = current_user.get("blocked", [])
            
    if not blocked:
        print("You have no blocked users.")
        input("Press Enter to go back...")

    print(", ".join(blocked))

    unblock_prompt = inquirer.confirm(message="Do you want to unblock someone?", default=False).execute()
            
    if unblock_prompt:
        to_unblock = inquirer.select(
            message="Select a user to unblock:",
            choices=blocked
        ).execute()
                
        current_user["blocked"].remove(to_unblock)
        users[to_unblock].setdefault("notifications", []).append(f"You were unblocked by {current_user['username']}.")
        users[current_user["username"]] = current_user
        save_dataa(users)
        print(f"User '{to_unblock}' has been unblocked.")
                

        input("Press Enter to go back...")
