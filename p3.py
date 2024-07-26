from cryptography.fernet import Fernet
import base64
import os
from hashlib import pbkdf2_hmac
from cryptography.fernet import InvalidToken  # Import specific exceptions from cryptography

# Function to derive a key from the master password using PBKDF2
def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = pbkdf2_hmac(
        hash_name='sha256',
        password=master_password.encode(),
        salt=salt,
        iterations=100000
    )
    return base64.urlsafe_b64encode(kdf)

# Load or generate the base key
def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    return key

# Load or generate the salt
def get_salt():
    if not os.path.exists("salt.salt"):
        salt = os.urandom(16)
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)
    else:
        with open("salt.salt", "rb") as salt_file:
            salt = salt_file.read()
    return salt

# Function to add a new password
def add():
    source = input("Enter the website/source: ")
    name = input("Enter the username: ")
    pwd = input("Enter the password: ")

    with open('passwords.txt', 'a') as f:
        encrypted_pwd = fer.encrypt(pwd.encode()).decode()
        f.write(source + " | " + name + " | " + encrypted_pwd + "\n")

# Function to view stored passwords
def view():
    try:
        with open('passwords.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                parts = data.split(" | ")
                if len(parts) == 3:
                    source, name, encrypted_pwd = parts
                    try:
                        decrypted_pwd = fer.decrypt(encrypted_pwd.encode()).decode()
                        print(f"Source: {source} | Username: {name} | Password: {decrypted_pwd}")
                    except InvalidToken:
                        print("Error: Incorrect master password or data corrupted.")
                        return
                else:
                    print(f"Skipping malformed line: {data}")
    except FileNotFoundError:
        print("No passwords saved yet.")

# Main code
master_pass = input("Enter the Master Password: ")
base_key = load_key()
salt = get_salt()

# Verify master password by trying to initialize Fernet
try:
    fernet_key = derive_key(master_pass, base_key + salt)
    fer = Fernet(fernet_key)
    print("Master password accepted. You can now view or add passwords.")
except InvalidToken:
    print("Invalid master password. Please try again.")
    exit(1)

while True:
    mode = input("Enter what you want to do (add/view) or 'q' to quit: ").lower()
    if mode == "q":
        break
    elif mode == "add":
        add()
    elif mode == "view":
        view()
    else:
        print("Invalid option. Please enter 'add' or 'view'.")
