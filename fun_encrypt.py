from cryptography.fernet import Fernet
import json 
import requests
import os 

#Encrypt User 
def encrypt_user():
    with open('user.txt') as f:
        user_data = ''.join(f.readlines())

### 2. generate key and write it in a file
    key = Fernet.generate_key()
    f = open("refUserKey.txt", "wb")
    f.write(key)
    
### 3. encrypt the user and write it in a file
    refKey = Fernet(key)
    user_data_byt = bytes(user_data, 'utf-8') # convert into byte
    encryptedUser = refKey.encrypt(user_data_byt)

    f = open("encryptedUser.txt", "wb")
    f.write(encryptedUser)
    f.close()

### 4. delete the password file
    if os.path.exists("user.txt"):
        os.remove("user.txt")
    else:
        print("File is not available")

##Encrypt Password
def encrypt_pwd():    #### 1. read your password file
    with open('pwd.txt') as f:
        mypwd = ''.join(f.readlines())
    
### 2. generate key and write it in a file
    key = Fernet.generate_key()
    f = open("refPwdKey.txt", "wb")
    f.write(key)
    f.close()

### 3. encrypt the password and write it in a file
    refKey = Fernet(key)
    mypwdbyt = bytes(mypwd, 'utf-8') # convert into byte
    encryptedPWD = refKey.encrypt(mypwdbyt)
    f = open("encryptedPWD.txt", "wb")
    f.write(encryptedPWD)
    f.close()
### 4. delete the password file
    if os.path.exists("pwd.txt"):
        os.remove("pwd.txt")
    else:
        print("File is not available")


if os.path.exists("user.txt") and os.path.exists('pwd.txt'):
    encrypt_user()
    encrypt_pwd()
else:
    print('Credentials are already encrypted , No Action Required')