
def yes_or_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer == "yes" or answer == "y" or answer == "Yes" or answer == "Y":
            return True
        elif answer == "no" or answer == "n" or answer == "No" or answer == "N":
            return False
        else:
            print("Please enter 'y/yes' or 'n/no'.")
            
print(yes_or_no('m'))