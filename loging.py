
import sign_up
users = {}
def login():
    print("\n----- Login -----")
    try:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        user = users.get(username)
        if user and user["password"] == password:
            print("Logged in successfully.")
            return user
        else:
            print("Invalid username or password.")
            return None
    except Exception as e:
        print("Error during login:", e)
        return None

