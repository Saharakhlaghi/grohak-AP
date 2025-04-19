from InquirerPy import inquirer
import sign_up
import login
import save_data
from home import home_menu

def main():
    users = save_data.load_dataa()
    current_user = None

    while True:
        choice = inquirer.select(
            message="Welcome! Please choose an option:",
            choices=["Sign Up", "Log In", "Exit"],
        ).execute()

        if choice == "Sign Up":
            user = sign_up.sign_up()
            if user:
                current_user = user
                break

        elif choice == "Log In":
            user = login.login()
            if user:
                current_user = user
                break

        elif choice == "Exit":
            print("Goodbye!")
            return

    home_menu(current_user)
    save_data.save_dataa(users)

if __name__ == "__main__":
    main()
