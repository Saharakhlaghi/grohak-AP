from InquirerPy import inquirer
import sign_up
import login
import save_data
from home import *
from profilee import *
from search import *
import chat_storage

def main():
    users = save_data.load_dataa()      
    current_user = None

    while True:
        choice = inquirer.select(
            message="Welcome! Please choose an option:",
            choices=["Sign Up", "Log In","Exit"],
        ).execute()

        if choice == "Sign Up":
            user = sign_up.sign_up()
            if user:
                current_user = user
            

        elif choice == "Log In":
            user = login.login()
            if user:
                current_user = user
                while True:
                    users=load_dataa()
                    current_user=users[current_user["username"]]
                    users={}
                    choice = inquirer.select(
                        message="Welcome! Please choose an option:",
                        choices=["Home", "Profile", "Search", "Exit"],
                    ).execute()
                    
                    if choice=="Home":
                        home_menu(current_user)
                    elif choice == "Profile":
                        profile_menu(current_user)
                    elif choice == "Search":
                        search_menu(current_user)
                    elif choice == "Exit":
                        
                        break

        elif choice == "Exit":
            print("Goodbye!")
            return
        
        
    
save_data.save_dataa(users)

main()
