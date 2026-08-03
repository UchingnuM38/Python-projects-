import random
import string
import os
import hashlib
import getpass
from cryptography.fernet import Fernet

# ---------- FILE NAME ----------
DATA_FILE = "passwords.enc"
KEY_FILE = "secret.key"
MASTER_FILE = "master.hash"


print(" ---------- Encryption Key ----------")
def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key


# ---------- Master Password ----------
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()


def setup_master_password():
    print("Set up master password")
    while True:
        pwd1 = getpass.getpass("Master Password: ")
        pwd2 = getpass.getpass("Write again: ")
        if pwd1 == pwd2 and pwd1.strip() != "":
            with open(MASTER_FILE, "w") as f:
                f.write(hash_password(pwd1))
            print("Master Password are set!\n")
            return
        else:
            print("Not valid please try again\n")


def verify_master_password():
    with open(MASTER_FILE, "r") as f:
        saved_hash = f.read().strip()
    for _ in range(3):
        pwd = getpass.getpass("Master Password : ")
        if hash_password(pwd) == saved_hash:
            print("Access Granted!\n")
            return True
        else:
            print("Invalid password। Please try again")
    return False


# ---------- Encrypt/Decrypt ----------
def load_passwords(fernet):
    passwords = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    decrypted = fernet.decrypt(line).decode()
                    site, pwd = decrypted.split(":", 1)
                    passwords[site] = pwd
                except Exception:
                    continue
    return passwords


def save_password_entry(fernet, site, pwd):
    entry = f"{site}:{pwd}"
    encrypted = fernet.encrypt(entry.encode())
    with open(DATA_FILE, "ab") as f:
        f.write(encrypted + b"\n")


def rewrite_all_passwords(fernet, passwords):
    with open(DATA_FILE, "wb") as f:
        for site, pwd in passwords.items():
            entry = f"{site}:{pwd}"
            encrypted = fernet.encrypt(entry.encode())
            f.write(encrypted + b"\n")


# ---------- Password Generator ----------
def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+?/.,"
    return "".join(random.choice(chars) for _ in range(length))


# ---------- Password Strength Checker ----------
def check_strength(pwd):
    score = 0
    if len(pwd) >= 8:
        score += 1
    if len(pwd) >= 12:
        score += 1
    if any(c.islower() for c in pwd) and any(c.isupper() for c in pwd):
        score += 1
    if any(c.isdigit() for c in pwd):
        score += 1
    if any(c in "!@#$%^&*()_+?/.," for c in pwd):
        score += 1

    if score <= 2:
        return "Weak password"
    elif score in (3, 4):
        return "Medium password"
    else:
        return "Strong password"


# ---------- Main Program ----------
def main():
    if not os.path.exists(MASTER_FILE):
        setup_master_password()
    else:
        if not verify_master_password():
            print("Invalid...!")
            return

    key = load_or_create_key()
    fernet = Fernet(key)
    passwords = load_passwords(fernet)

    while True:
        print("\n----- PERSONAL PASSWORD MANAGER -----")
        print("1. Save Password")
        print("2. View Password")
        print("3. Generate Password")
        print("4. Delete Password")
        print("5. Exit")

        choice = input("Enter Your choice: ").strip()

        if choice == "1":
            site = input("Enter your website: ").strip()
            pwd = input("Enter your password: ").strip()
            if pwd == "":
                pwd = generate_password()
                print(f"Auto-generated password: {pwd}")
            passwords[site] = pwd
            save_password_entry(fernet, site, pwd)
            print(f"'{site}' Password saved!... Strength: {check_strength(pwd)}")

        elif choice == "2":
            if not passwords:
                print("No data")
            else:
                print("\n--- Saved Passwords ---")
                for site, pwd in passwords.items():
                    print(f"{site} : {pwd}")

        elif choice == "3":
            try:
                length = int(input("Enter the lenght of password: ") or 16)
            except ValueError:
                length = 16
            new_pwd = generate_password(length)
            print(f"Generated Password: {new_pwd}")
            print(f"Strength: {check_strength(new_pwd)}")

        elif choice == "4":
            site = input("Enter Your website: ").strip()
            if site in passwords:
                del passwords[site]
                rewrite_all_passwords(fernet, passwords)
                print(f"'{site}' Deleted Password\n")
            else:
                print("Not valid....!")

        elif choice == "5":
            print("ok bye..!")
            break

        else:
            print("Not valid! Pease try again")


if __name__ == "__main__":
    main()