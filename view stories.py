def view_stories(current_user):
    print(" Stories ")
        
    found = False
    for uname, user in users.items():
        if uname["username"] in current_user["following"]:
            if uname != current_user["username"] and uname not in current_user["blocked"]:
                if user["stories"]:
                    for idx, story in enumerate(user["stories"]):
                        print(f"\n{uname}'s Story #{idx+1}:")
                        print(f"{story['content']}")
                        print(f"Likes: {story['Likes']}")
                            
                        action = inquirer.select(
                            message="",
                            choices=["Like", "Unlike", "Skip"],
                        ).execute()
                            
                        already_liked= current_user["username"] in story["liked_by"]
                            
                        if action == "Like":
                            if not already_liked:
                                story["likes"] += 1
                                story["liked_by"].add(current_user["username"])
                                print("Story liked.")
                                #notification?
                            else:
                                print("You've already liked this story.")
                                
                        elif action == "Unlike":
                            if already_liked:
                                story["likes"] -= 1
                                story["liked_by"].remove(current_user["username"])
                                print("Story unliked.")
                            else:
                                print("You haven't liked this story.")
                                
                        elif action == "Skip":
                            print("Skipped.")
                                
                        found = True
        if not found:
            print("No stories available.")
                
        input("\nPress Enter to go back...")
    
    #watched, unwatched stories???