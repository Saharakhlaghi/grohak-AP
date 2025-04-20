
import yes_or_no
import save_data
def password_test(password):
    Flag_1 = False
    Flag_2 = False
    Flag_3 = False
    Flag_4 = False

    for i in password:
        cod = ord(i)
        if 65 <= cod <= 90:
            Flag_1 = True
        if 97 <= cod <= 122:
            Flag_2 = True
        if 48 <= cod <= 57:
            Flag_3 = True
        if cod == 64 or cod == 63 or cod == 33 or cod == 38 or cod == 95 or cod == 35 or cod == 36:
            Flag_4 = True
    
    if Flag_1 and Flag_2 and Flag_3 and Flag_4:
        return True
    else:
        print("Use lowercase and uppercase letters, numbers, and @/?/!/&/_/#/$")
        return False

users =save_data.load_dataa() 

def sign_up():
    print("\n----- Sign Up -----")
    try:
        email = input("email: ").strip()
        
        if not email.endswith("@gmail.com"):
            print("Email must end with << @gmail.com >>")
            return None

        for user in users.values():
            if user["email"] == email:
                print("This email is already registered.")
                return None
            
        username = input("Username: ").strip()
        if username in users:
            print("This username is already taken.")
            return None
        
        password_input = input("Password: ").strip()
        
        while not password_test(password_input):
            password_input = input("Password: ").strip()
        
        full_name = input("Full Name: ").strip()
        bio = input("Bio: ").strip()
        is_private = yes_or_no.yes_or_no("Make profile private? (y/n): ")
        user_data = {
            "email": email,
            "username": username,
            "password": password_input,
            "full_name": full_name,
            "bio": bio,
            "is_private": is_private,
            "posts": [],
            "stories":[],
            "followers": [],
            "following": [],
            "notifications": [],
            "notification_history": [],
            "follow_requests": [],
            "saved_posts": [],
            "blocked": []
        }

        users[username] = user_data
        print("Account created successfully. You are now logged in.")
        save_data.save_dataa(users)
        return user_data
    
    except Exception as e:
        print("Error during registration:", e)
        return None
