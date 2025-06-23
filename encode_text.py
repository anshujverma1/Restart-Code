from cryptography.fernet import Fernet
import os

# def encrypt(content):
#     pass

# if os.path.exists("user.txt"):
#     with open("user.txt") as file:
#         content=file.read()
#         encrypt(content)

from cryptography.fernet import Fernet

# Generate a key once and save it securely
key = Fernet.generate_key()
print("Save this key securely:", key.decode())

fernet = Fernet(key)
plain_password = input("Enter password to encrypt: ")
encrypted = fernet.encrypt(plain_password.encode())
print("Encrypted password to paste in config.properties:", encrypted.decode())
