from InquirerPy import inquirer
import save_data
import search
import json
import os
from datetime import datetime
from profilee import *
from chat_storage import load_chats, save_chats
users =save_data.load_dataa()
 
def home_menu(current_user):
    while True:
        choice = inquirer.select(
            message=" Home ",
            choices=[
                "Stories",
                "Posts",
                "Messages", 
                "Notifications",
                "Shared Posts",
                "Back"
            ],   
        ).execute()
      
        if choice == "Stories":
            view_stories(current_user)
        elif choice == "Posts":
            view_posts(current_user)
        elif choice == "Messages":
            view_messages(current_user)
        elif choice == "Notifications":
            notifications(current_user)
        elif choice == "Shared Posts":
            view_shared_posts(current_user)
        elif choice == "Back":
            break
        

def view_stories(current_user):
    print("---Stories--- ")
    users = load_dataa()
    found = False

    for uname, user in users.items():
        if uname in current_user["following"]:
            if uname != current_user["username"] and uname not in current_user["blocked"]:
                if user.get("stories"):
                    for idx, story in enumerate(user["stories"]):
                        print(f"\n{uname}'s Story #{idx+1}:")
                        print(f"{story['content']}")
                        print(f"Likes: {story['likes']}")
                        
                        action = inquirer.select(
                            message="",
                            choices=["Like", "Unlike", "Skip"],
                        ).execute()
                        
                        already_liked = current_user["username"] in story.get("liked_by", [])
                        
                        if action == "Like":
                            if not already_liked:
                                story["likes"] += 1
                                story["liked_by"].append(current_user["username"])
                                print("Story liked.")
                                user["notifications"].append(f"{current_user['username']} liked your story.")
                                save_data.save_dataa(users)
                            else:
                                print("You've already liked this story.")
                        
                        elif action == "Unlike":
                            if already_liked:
                                story["likes"] -= 1
                                story["liked_by"].remove(current_user["username"])
                                print("Story unliked.")
                                save_data.save_dataa(users)
                            else:
                                print("You haven't liked this story.")
                        
                        elif action == "Skip":
                            print("Skipped.")
                        
                        found = True

    if not found:
        print("No stories available.")
        input("\nPress Enter to go back...")

        
all_posts=[]  
def view_posts(current_user):
    print("---Posts---")

    for uname, user in users.items():
        if uname in current_user["following"]:
            if uname != current_user["username"] and uname not in current_user["blocked"]:
                for post in user["posts"]:
                    # Convert string post to dict if needed
                    if isinstance(post, str):
                        post = {
                            "content": post,
                            "likes": 0,
                            "comments": [],
                            "shares": 0,
                            "saves": 0,
                            "liked_by": []
                        }
                    all_posts.append((uname, post))

    if not all_posts:
        print("No posts available.")
        input("Press Enter to go back...")
        return
    
    while True:
        choices = [
            {
                "name": f"{idx+1}. {owner}: {post['content'][:30]} "
                        f"(Likes: {post['likes']} | Comments: {len(post['comments'])} | Shares: {post['shares']} | Saves: {post['saves']})",
                "value": idx
            }
            for idx, (owner, post) in enumerate(all_posts)
        ]
        choices.append({"name": " Back ", "value": "back"})
        
        selected = inquirer.select(
            message="Select the post you want to view.",
            choices=choices,
        ).execute()
        
        if selected == "back":
            break
        
        post_owner, post = all_posts[selected]

        print("\n--- Post Details ---")
        print(f"From: {post_owner}")
        print(f"Content: {post['content']}")
        print(f"Likes: {post['likes']} | Comments: {len(post['comments'])} | Shares: {post['shares']} | Saves: {post['saves']} | Time: {post['time']}")

        if post["comments"]:
            print("\n--- Comments ---")
            for i, (commenter, comment) in enumerate(post["comments"], 1):
                print(f"{i}. {commenter}: {comment}")
        else:
            print("\nNo comments yet.")

        print()

        action = inquirer.select(
            message="Choose an action:",
            choices=["Like", "Comment", "Save", "Share", "Back"],
        ).execute()
        
        if action == "Like":
            if current_user["username"] not in post["liked_by"]:
                post["likes"] += 1
                post["liked_by"].append(current_user["username"])
                print("Post liked.")
                users[post_owner]["notifications"].append(f"{current_user['username']} liked your post.")
                save_data.save_dataa(users)
            else:
                post["likes"] -= 1
                post["liked_by"].remove(current_user["username"])
                print("Post unliked.")
                save_data.save_dataa(users)
        
        elif action == "Comment":
            comment = input("Enter your comment: ").strip()
            if comment:
                post["comments"].append((current_user["username"], comment))
                users[post_owner]["notifications"].append(f"{current_user['username']} commented on your post.")
                for word in comment.split():
                    if word.startswith("@"):
                        tagged = word[1:]
                        if tagged in users:
                            users[tagged]["notifications"].append(f"{current_user['username']} tagged you in a post.")
                print("Comment added.")
                save_data.save_dataa(users)
        
        elif action == "Save":
            if post not in current_user["saved_posts"]:
                current_user["saved_posts"].append(post)
                post["saves"] += 1
                print("Post saved.")
                users[current_user["username"]] = current_user
                save_data.save_dataa(users)
            else:
                print("Post already saved.")
        
        elif action == "Share":
            recipient = input("Enter the username you want to share this post with: ").strip()
            if recipient in users and recipient != current_user["username"]:
                users[recipient].setdefault("shared_posts", []).append({
                    "from": current_user["username"],
                    "owner": post_owner,
                    "post": post
                })
                users[recipient]["notifications"].append(f"{current_user['username']} shared a post with you.")
                post["shares"] += 1
                print("Post shared.")
                save_data.save_dataa(users)
            else:
                print("Invalid username")

        
        elif action == "Back":
            continue
def view_shared_posts(current_user):
    print("---Shared Posts---")

    shared = current_user.get("shared_posts", [])
    if not shared:
        print("No posts have been shared with you.")
        input("Press Enter to go back...")
        return

    for idx, shared_info in enumerate(shared, 1):
        from_user = shared_info["from"]
        owner = shared_info["owner"]
        post = shared_info["post"]

        print(f"{idx}. Shared by {from_user} | Original post by {owner}")
        print(f"   Content: {post['content']}")
        print(f"   Likes: {post['likes']} | Comments: {len(post['comments'])} | Shares: {post['shares']} | Saves: {post['saves']} | Time: {post['time']}")
        print()

    input("Press Enter to go back...")

      
def get_chat_key(user1, user2):
    return tuple(sorted([user1, user2]))

def view_messages(current_user):
    chats = load_chats()
    while True:
        print("---Messages---")   
        user_chats = [key for key in chats if current_user["username"] in key]
        options = []
        chat_lookup = {}

        if user_chats:
            for chat_key in user_chats:
                others = [uname for uname in chat_key if uname != current_user["username"]]
                if not others:
                    print("Could not identify the other user in chat.")
                    continue
                other = others[0]
                label = f"Chat with {other}"
                options.append(label)
                chat_lookup[label] = other
        else:
            print("No chats available.")

        options.extend(["Start a new chat", "Group Chats", "Back"])

        choice = inquirer.select(
            message="",
            choices=options,
        ).execute()

        if choice == "Start a new chat":
            available_users = [
                uname for uname in users
                if uname != current_user["username"]
                and uname not in current_user.get("blocked", [])
            ]
            if not available_users:
                print("No available users to chat with.")
                continue

            target_username = inquirer.select(
                message="Choose a user to chat with:",
                choices=available_users
            ).execute()

            chat_key = get_chat_key(current_user["username"], target_username)
            chats = load_chats()
            if chat_key not in chats:
                chats[chat_key] = []
                save_chats(chats)    
            chat_session(current_user, target_username, chat_key)

        elif choice == "Group Chats":
            group_chat_menu(current_user, users)

        elif choice == "Back":
            break

        else:
            target_username = chat_lookup[choice]
            chat_key = get_chat_key(current_user["username"], target_username)
            chat_session(current_user, target_username, chat_key)


def chat_session(current_user, target_username, chat_key):
    while True:
        chats = load_chats()
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
                chats.setdefault(chat_key, []).append((current_user["username"], msg))
                save_chats(chats)

                if "notifications" not in users[target_username]:
                    users[target_username]["notifications"] = []
                users[target_username]["notifications"].append(
                    f"New message from {current_user['username']}."
                )
                save_data.save_dataa(users)
                print("Message sent.")

        elif choice == "Back":
            break


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
    
    choices = [u for u in users.keys() if u != current_user["username"]]
    if not choices:
        print("No other users to add.")
        return

    members = inquirer.checkbox(message="Add members:", choices=choices).execute()
    groups[name] = {
        "members": [current_user["username"]] + members,
        "messages": []
    }
    save_groups(groups)
    print(f"Group '{name}' created.")

def join_group_chat(current_user, groups):
    available = [g for g, d in groups.items() if current_user["username"] not in d["members"]]
    if not available:
        print("No groups to join.")
        return
    
    name = inquirer.select(message="Join which group?", choices=available).execute()
    groups[name]["members"].append(current_user["username"])
    save_groups(groups)
    print(f"You joined '{name}'.")

def leave_group_chat(current_user, groups):
    member_of = [g for g, d in groups.items() if current_user["username"] in d["members"]]
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
            message=f"--- {name} ---",
            choices=[
                "View Messages",
                "Send Message",
                "Add Member",
                "Remove Member",
                "Leave Group",
                "Back"
            ]
        ).execute()

        if choice == "View Messages":
            view_group_messages(current_user, groups, name)

        elif choice == "Send Message":
            send_group_message(current_user, groups, name)

        elif choice == "Add Member":
            add_group_member(current_user, users, groups, name)

        elif choice == "Remove Member":
            remove_group_member(current_user, groups, name)
           
        elif choice == "Leave Group":
            leave_group_chat(current_user, groups)
            break

        elif choice == "Back":
            break

def add_group_member(current_user, users, groups, name):
    group = groups[name]
    if current_user["username"] not in group["members"]:
        print("You are not a member of this group.")
        return

    available_users = [u for u in users if u not in group["members"]]
    if not available_users:
        print("No users available to add.")
        return

    print("Available users to add:")
    for i, u in enumerate(available_users, 1):
        print(f"{i}. {u}")

    selected = input("Enter numbers of users to add (comma-separated): ").strip()
    if not selected:
        print("No users selected.")
        return

    try:
        selected_indices = [int(idx) - 1 for idx in selected.split(',')]
        new_members = [available_users[i] for i in selected_indices if 0 <= i < len(available_users)]
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return

    if not new_members:
        print("No valid users selected.")
        return

    group["members"].extend(new_members)
    save_groups(groups)
    print(f"Added {', '.join(new_members)} to '{name}'.")



def remove_group_member(current_user, groups, name):
    group = groups[name]
    if current_user["username"] not in group["members"]:
        print("You are not a member of this group.")
        return

    removable = [u for u in group["members"] if u != current_user["username"]]
    if not removable:
        print("No members you can remove.")
        return

    print("Current members:")
    for i, u in enumerate(removable, 1):
        print(f"{i}. {u}")

    to_remove = input("Enter numbers of members to remove (comma-separated): ").strip()
    if not to_remove:
        print("No members selected.")
        return

    try:
        remove_indices = [int(idx) - 1 for idx in to_remove.split(',')]
        members_to_remove = [removable[i] for i in remove_indices if 0 <= i < len(removable)]
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return

    if not members_to_remove:
        print("No valid members selected.")
        return

    for member in members_to_remove:
        group["members"].remove(member)

    save_groups(groups)
    print(f"Removed {', '.join(members_to_remove)} from '{name}'.")



def group_chat_menu(current_user, users):
    groups = load_groups()
    while True:
        choice = inquirer.select(
            message="--- Group Chats ---",
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

def notifications(current_user):
    print("---Notifications---")
    
    current_user.setdefault("other_notifs", [])
    current_user.setdefault("follow_requests", [])
    current_user.setdefault("notification_history", [])

    while True:
        tagged_count = count_tagged_posts(current_user)
        request_count = len(current_user["follow_requests"])
        other_count = len(current_user["notifications"]) 
        
        choices= [
            f"Tagged Posts ({tagged_count})",
            f"Follow Requests ({request_count})",
            f"Other ({other_count})",
            "History",
            "Back"
        ]
        
        choice = inquirer.select(
            message=" Notification ",
            choices=choices,
        ).execute()
        
        if choice == f"Tagged Posts ({tagged_count})":
            tagged_posts(current_user)
        elif choice == f"Follow Requests ({request_count})":
            follow_requests(current_user)
        elif choice == f"Other ({other_count})":
            other_notifs(current_user)
        elif choice == "History":
            print("Notification History")
            history = current_user.get("notification_history", [])
            if not history:
                print("No history available.")
            else:
                for item in history:
                    print("-", item)
            input("Press Enter to continue...")
            
        elif choice == "Back":
            break
         
def tagged_posts(current_user):
    print("---Tagged Posts---") 
    tagged_posts = []

    for uname, user in users.items():
        if uname in current_user.get("blocked", []):
            continue
        for post in user.get("posts", []):
            for commenter, comment in post.get("comments", []):
                if f"@{current_user['username']}" in comment:
                    tagged_posts.append((uname, post, commenter, comment))
                    current_user["notification_history"].append(
                        f"[tagged] Mentioned by {commenter} in a post by {uname}: '{comment}'"
                    )
                    break 

    if not tagged_posts:
        print("No tagged posts.")
    else:
        for idx, (owner, post, commenter, comment) in enumerate(tagged_posts):
            print(f"{idx+1}. Post by {owner}")
            print(f"{commenter} tagged you in a comment: \"{comment}\"")
            print(f"Post content: {post['content']}")
            print(f"Likes: {post['likes']} | Comments: {len(post['comments'])} | Shares: {post['shares']} | Saves: {post['saves']}")
    
    input("Press Enter to continue...")


        
def count_tagged_posts(current_user):
    count = 0
    for uname, user in users.items():
        if uname in current_user["blocked"]:
            continue
        for post in user["posts"]:
            if isinstance(post["comments"], list):
                for comment_tuple in post["comments"]:
                    if isinstance(comment_tuple, tuple) and len(comment_tuple) == 2:
                        commenter, comment = comment_tuple
                        if f"@{current_user['username']}" in comment:
                            count += 1
                            break  
            else:
                if isinstance(post["comments"], str) and f"@{current_user['username']}" in post["comments"]:
                    count += 1

    return count

    
def follow_requests(current_user):
    print(" Follow Requests ")
    if not current_user["follow_requests"]:
        print("No follow requests.")
    else:
        requests = list(current_user["follow_requests"])
        users = save_data.load_dataa() 

        for requester in requests:
            print(f"Follow request from: {requester}")
            answer = inquirer.select(
                message=f"Do you want to accept {requester}'s follow request?",
                choices=["Accept", "Reject"],
                default="Reject"
            ).execute()

            if answer == "Accept":
                if requester not in current_user["followers"]:
                    current_user["followers"].append(requester)
                    users[current_user["username"]] = current_user
                    save_data.save_dataa(users)
                if requester in users:
                    if current_user["username"] not in users[requester]["following"]:
                        users[requester]["following"].append(current_user["username"])
                        users[requester]["notifications"].append(
                            f"Your follow request to {current_user['username']} was accepted."
                        )
                        current_user["notification_history"].append(
                            f"[Follow Request] Accepted {requester}'s follow request"
                        )
                        save_data.save_dataa(users) 
                print(f"{requester} is now a follower.")
            else:
                if requester in users:
                    users[requester]["notifications"].append(
                        f"Your follow request to {current_user['username']} was rejected."
                    )
                current_user["notification_history"].append(
                    f"[Follow Request] Rejected {requester}'s follow request"
                )
                print(f"Follow request from {requester} rejected.")
                save_data.save_dataa(users)

        current_user["follow_requests"] = []
        users=save_data.load_dataa()
        users[current_user["username"]]=current_user
        save_data.save_dataa(users)

    input("Press Enter to continue...")
    
    
def other_notifs(current_user):
    print("---Other Notificatons---")
    
    if not current_user["notifications"]:
        print("No notifications.")
    else: 
        for note in current_user["notifications"]:
            print("-", note)
            current_user["notification_history"].append(f"[Other] {note}")
        current_user["notifications"]=[]
        users=save_data.load_dataa()
        users[current_user["username"]]=current_user
        save_data.save_dataa(users)
        input("Press Enter to continue...")
            