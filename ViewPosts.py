from InquirerPy import inquirer

def view_posts(current_user):
    print("\n Posts ")
    
    all_posts = []
    for uname, user in users.items():
        if uname["username"] in current_user["following"]:
                if uname != current_user["username"] and uname not in current_user["blocked"]:
                    for post in user["posts"]:
                        all_posts.append((uname,post))
    if not all_posts:
        print("No posts available.")
        input("Press Enter to go back...")
        return
    
    #!
    while True:
        choices = [
            {
                "name": f"{idx+1}. {owner}: {post['content'][:30]}",
                "value": idx
            }
            for idx, (owner, post) in enumerate(all_posts)
        ]
        choices.append({"name": " Back ", "value": "back"})
        
        selected = inquirer.select(
            message = "Select the post you want to view.",
            choices = choices,
        ).execute()
        
        if selected == "back":
            break
        
        post_owner, post = all_posts[selected]
        action = inquirer.select(
            message="",
            choices=["Like", "Comment", "Save", "Share", "Back"],
        ).execute()
        
        if action == "Like":
            if current_user["username"] not in post["liked_by"]:
                post["likes"] += 1
                post["liked_by"].add(current_user["username"])
                print("Post liked.")
                users[post_owner]["notifications"].append(f"{current_user['username']} liked your post.")
            else:
                post["likes"] -= 1
                post["liked_by"].remove(current_user["username"])
                print("Post unliked.")
            
        elif action == "Comment":
            comment = input("Enter your comment: ").strip()
            post["comments"].append((current_user["username"], comment))
            users[post_owner]["notifications"].append(f"{current_user['username']} commented on your post.")
            for word in comment.split():
                if word.startswith("@"):
                    tagged = word[1:]
                    if tagged in users:
                        users[tagged]["notifications"].append(f"{current_user['username']} tagged you in a post.")
            print("Comment added.")            
            
        elif action == "Save":
            if post not in current_user["saved_posts"]:
                current_user["saved_posts"].append(post)
                post["saves"] += 1
                print("Post saved.")
            else:
                print("Post already saved.")
            
        elif action == "Share":
            recipient = input("Enter the username you want to share this post with: ").strip()
            if recipient in users and recipient != current_user["username"]:
                users[recipient]["notifications"].append(f"{current_user['username']} shared a post with you.")
                post["shares"] += 1
                print("Post shared.")
            else:
                print("Invalid username")
            
        elif action == "Back":
            break