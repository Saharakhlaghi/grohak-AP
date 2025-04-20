import save_data
def login():
    print("\n----- Login -----")
    try:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        users=save_data.load_dataa()
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

