def tagged_posts(current_user):
    print(" Tagged Posts ") 
    tagged_posts = []
    for uname, user in users.items():
        if uname in current_user["blocked"]:
            continue
        for post in user["posts"]:
            for commenter, comment in post["comments"]:
                if f"@{current_user['username']}" in comment:
                    tagged_posts.append((uname, post))
                    current_user["notification_history"].append(f"[tagged] Mentioned by {uname} in: '{post['content']}'")
                break
    if not tagged_posts:
        print("No tagged posts.")
        
    else:
        for idx, (owner, post) in enumerate(tagged_posts):
            print(f"{idx+1}. {owner}: {post['content']}")
            print(f"Likes: {post['likes']} | Comments: {len(post['comments'])} | Shares: {post['shares']} | Saves: {post['saves']}")
    input("Press Enter to continue...")
        
def count_tagged_posts(current_user):
    count = 0
    for uname, user in users.items():
        for uname, user in users.items():
            if uname in current_user["blocked"]:
                continue
            for post in user["posts"]:
                for commenter, comment in post["comments"]:
                    if f"@{current_user['username']}" in comment:
                        count += 1
                        break
    return count