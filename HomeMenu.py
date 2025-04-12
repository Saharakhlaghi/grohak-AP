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
            stories(current_user)
        elif choice == " Posts ":
            posts(current_user)
        elif choice == " Messages ":
            messages(current_user)
        elif choice == " Notifications ":
            notifications(current_user)
            break