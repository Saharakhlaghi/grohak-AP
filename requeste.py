

from InquirerPy import inquirer
import save_data

def follow_requests(current_user):
    print("\n--- Follow Requests ---")
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
                current_user["followers"].add(requester)
                if requester in users:
                    users[requester]["following"].add(current_user["username"])
                    users[requester]["notifications"].append(
                        f"Your follow request to {current_user['username']} was accepted."
                    )
                current_user["notification_history"].append(
                    f"[Follow Request] Accepted {requester}'s follow request"
                )
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
            current_user["follow_requests"].remove(requester)

    input("Press Enter to continue...")
