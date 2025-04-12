from InquirerPy import inquirer

def home_menu(current_user):
    while True:
        choice = inquirer.select(
            message=" Home ",
            choices=[
                " Stories ",
                " Posts ",
                " Messages ", # +group chat
                " Notifications ", # +tagged post
                " Back "
            ],   
            
        ).execute()
      
        if choice == " Stories ":
            view_stories(current_user)
        elif choice == " Posts ":
            view_posts(current_user)
        elif choice == " Messages ":
            view_messages(current_user)
        elif choice == " Notifications ":
            notifications(current_user)
            break
