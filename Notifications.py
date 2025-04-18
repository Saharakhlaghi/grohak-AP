def notifications(current_user):
    print(" Notifications ")
    
    while True:
        tagged_count = count_tagged_posts(current_user)
        request_count = len(current_user["follow_requests"])
        other_count = len(current_user["other_notifs"]) 
        
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
        
        
def other_notifs(current_user):
    print(" Other Notificatons ")
    
    if not current_user["notifications"]:
        print("No notifications")
    else: 
        for note in current_user["notifications"]:
            print("-", note)
            current_user["notificatin_history"].append(f"[Other] {note}")
        current_user["notifications"].clear()
        input("Press Enter to continue...")