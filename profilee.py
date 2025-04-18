from InquirerPy import inquirer
from InquirerPy.separator import Separator
from datetime import datetime

instagram_account = {
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
def yes_or_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ["yes", "y"]:
            return True
        elif answer in ["no", "n"]:
            return False
        else:
            print("Please enter 'y/yes' or 'n/no'.")

def view_my_profile():
    print(f"\n=== {instagram_account['username']}'s PROFILE ===")
    print(f"Bio: {instagram_account['bio']}")
    print(f"Posts: {len(instagram_account['posts'])}")
    print(f"Followers: {len(instagram_account['followers'])}")
    print(f"Following: {len(instagram_account['following'])}")
    
    print("\nRecent Posts:")
    for post in instagram_account['posts'][-3:]:
        print(f"- {post['content']} ({post['likes']} likes)")
    
    print("\n1. Edit Profile")
    print("2. View All Posts")
    print("0. Back to Main Menu")
    
    choice = input("Choose an option: ")
    if choice == "1":
        edit_profile()
    elif choice == "2":
        view_all_posts()

def create_new_post():
    print("\n=== CREATE NEW POST ===")
    content = input("What would you like to post? ")
    post_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    
    new_post = {
        "id": len(instagram_account["posts"]) + 1,
        "content": content,
        "likes": 0,
        "comments": [],
        "time": post_time  
    }
    
    instagram_account["posts"].append(new_post)
    print(f"\nYour post has been shared at {post_time}!")

def create_story():
    print("\n=== CREATE STORY ===")
    content = input("What's your story about? ")
    story_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    
    new_story = {
        "id": len(instagram_account.get("stories", [])) + 1,
        "content": content,
        "time": story_time,  
        "views": 0
    }
    
    if "stories" not in instagram_account:
        instagram_account["stories"] = []
    instagram_account["stories"].append(new_story)
    print(f"\nYour story has been posted at {story_time}!")

def view_followers():
    print("\n=== YOUR FOLLOWERS ===")
    if not instagram_account["followers"]:
        print("You don't have any followers yet.")
        return
    
    for i, follower in enumerate(instagram_account["followers"], 1):
        print(f"{i}. {follower}")
    
    print("\n1. View Follower Profile")
    print("0. Back to Main Menu")
    
    choice = input("Choose an option: ")
    if choice == "1":
        follower_num = input("Enter follower number: ")
        if follower_num.isdigit():
            num = int(follower_num) - 1
            if 0 <= num < len(instagram_account["followers"]):
                view_user_profile(instagram_account["followers"][num])

def view_following():
    print("\n=== ACCOUNTS YOU FOLLOW ===")
    if not instagram_account["following"]:
        print("You're not following anyone yet.")
        return
    
    for i, user in enumerate(instagram_account["following"], 1):
        print(f"{i}. {user}")
    
    print("\n1. View Profile")
    print("2. Unfollow User")
    print("0. Back to Main Menu")
    
    choice = input("Choose an option: ")
    if choice == "1":
        user_num = input("Enter user number: ")
        if user_num.isdigit():
            num = int(user_num) - 1
            if 0 <= num < len(instagram_account["following"]):
                view_user_profile(instagram_account["following"][num])
    elif choice == "2":
        unfollow_user()

def unfollow_user():
    print("\n=== UNFOLLOW USER ===")
    if not instagram_account["following"]:
        print("You're not following anyone yet.")
        return
    
    print("Accounts you follow:")
    for i, user in enumerate(instagram_account["following"], 1):
        print(f"{i}. {user}")
    
    while True:
        choice = input("\nEnter user number to unfollow (or 0 to cancel): ")
        if choice == "0":
            return
        if choice.isdigit():
            num = int(choice) - 1
            if 0 <= num < len(instagram_account["following"]):
                user = instagram_account["following"][num]
                if yes_or_no(f"Are you sure you want to unfollow {user}? (y/n): "):
                    instagram_account["following"].pop(num)
                    print(f"You have unfollowed {user}")
                return
        print("Invalid input. Please try again.")

def view_user_profile(username):
    print(f"\n=== {username}'s PROFILE ===")
    
    if username in other_accounts:
        user = other_accounts[username]
        print(f"Posts: {len(user['posts'])}")
        print(f"Followers: {len(user['followers'])}")
        print(f"Following: {len(user['following'])}")
        
        if username in instagram_account["following"]:
            print("\n1. Unfollow")
        else:
            print("\n1. Follow")
        
        print("2. Send Message")
        print("0. Back")
        
        choice = input("Choose an option: ")
        if choice == "1":
            if username in instagram_account["following"]:
                if yes_or_no(f"Are you sure you want to unfollow {username}? (y/n): "):
                    instagram_account["following"].remove(username)
                    print(f"You unfollowed {username}")
            else:
                if yes_or_no(f"Do you want to follow {username}? (y/n): "):
                    instagram_account["following"].append(username)
                    print(f"You followed {username}")
        elif choice == "2":
            send_message(username)
    else:
        print("User not found.")

def delete_account():
    print("\n=== DELETE ACCOUNT ===")
    print("WARNING: This will permanently delete your account and all data!")
    
    if not yes_or_no("Are you sure you want to continue? (y/n): "):
        print("Account deletion cancelled.")
        return False
    
    password = input("Enter your password to confirm: ")
    if password != instagram_account["password"]:
        print("Incorrect password. Deletion cancelled.")
        return False
    
    if not yes_or_no("This action cannot be undone. Are you absolutely sure? (y/n): "):
        print("Account deletion cancelled.")
        return False
    
    instagram_account["username"] = "[deleted]"
    instagram_account["posts"].clear()
    instagram_account["followers"].clear()
    instagram_account["following"].clear()
    
    print("\nYour account has been permanently deleted.")
    return True
    
def edit_profile(): pass
def view_all_posts(): pass
def send_message(user): pass
def view_notifications(): pass
def view_messages(): pass
def account_settings(): pass
def search_users(): pass

def show_main_menu():
    choice = inquirer.select(
        message=f"=== INSTAGRAM MAIN MENU ===\nLogged in as: {instagram_account['username']}",
        choices=[
            {"name": "1. View My Profile", "value": 1},
            {"name": "2. Create New Post", "value": 2},
            {"name": "3. Create Story", "value": 3},
            {"name": "4. View Followers", "value": 4},
            {"name": "5. View Following", "value": 5},
            {"name": "6. Search Users", "value": 6},
            {"name": "7. View Notifications", "value": 7},
            {"name": "8. View Messages", "value": 8},
            {"name": "9. Account Settings", "value": 9},
            Separator(),
            {"name": "10. Logout", "value": 10},
            {"name": "11. Delete Account", "value": 11},
        ],
        pointer=">",
    ).execute()
    
    return choice

def main():
    while True:
        choice = show_main_menu()
        
        if choice == 1:
            view_my_profile()
        elif choice == 2:
            create_new_post()
        elif choice == 3:
            create_story()
        elif choice == 4:
            view_followers()
        elif choice == 5:
            view_following()
        elif choice == 6:
            search_users()
        elif choice == 7:
            view_notifications()
        elif choice == 8:
            view_messages()
        elif choice == 9:
            account_settings()
        elif choice == 10:
            if yes_or_no("Are you sure you want to logout? (y/n): "):
                print("\nYou have been logged out.")
                break
        elif choice == 11:
            if delete_account():
                break
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
