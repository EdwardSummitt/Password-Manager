import json
import os
from getpass import getpass
from cryptography.fernet import Fernet

def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as f:
            f.write(key)
    else:
        with open("key.key", "rb") as f:
            key = f.read()
    return key

def encrypt_password(password, fernet):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(password, fernet):
    return fernet.decrypt(password.encode()).decode()

def load_passwords():
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as f:
            return json.load(f)
    return {}

def save_passwords(data):
    with open("passwords.json", "w") as f:
        json.dump(data, f, indent=2)

def main():
    key = load_key()
    fernet = Fernet(key)

    passwords = load_passwords()

    while True:
        print("\nPassword Manager")
        print("1. Add new credential")
        print("2. Get credential")
        print("3. List sites")
        print("4. Delete credential")
        print("5. Exit")
        choice = input("Choice: ")

        if choice == "1":
            site = input("Site: ")
            username = input("Username: ")
            password = getpass("Password: ")
            passwords[site] = {
                "username": username,
                "password": encrypt_password(password, fernet)
            }
            save_passwords(passwords)
            print("Saved!")

        elif choice == "2":
            site = input("Site: ")
            if site in passwords:
                username = passwords[site]["username"]
                password = decrypt_password(passwords[site]["password"], fernet)
                print(f"Username: {username}")
                print(f"Password: {password}")
            else:
                print("No entry for that site.")

        elif choice == "3":
            print("Sites:", ", ".join(passwords.keys()) or "None")

        elif choice == "4":
            site = input("Site to delete: ")
            if site in passwords:
                del passwords[site]
                save_passwords(passwords)
                print("Deleted.")
            else:
                print("No entry found.")

        elif choice == "5":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

            


