from cryptography.fernet import Fernet
import json 
import requests
import os 

#Decrypt User 
def decrypt_user():
    with open('encryptedUser.txt') as f:
        encuser = ''.join(f.readlines())
        encuserbyt = bytes(encuser, 'utf-8')
    
# read key and convert into byte
    with open('refUserKey.txt') as f:
        refKey = ''.join(f.readlines())
        refKeybyt = bytes(refKey, 'utf-8')

# use the key and encrypt pwd
    keytouse = Fernet(refKeybyt)
    myUser = (keytouse.decrypt(encuserbyt))

    usr_dec=myUser.decode(encoding='utf=8')
    return usr_dec

#Decrypt Pwd
def decrypt_pwd():
    with open('encryptedPWD.txt') as f:
        encpwd = ''.join(f.readlines())
        encpwdbyt = bytes(encpwd, 'utf-8')
    
# read key and convert into byte
    with open('refPwdKey.txt') as f:
        refKey = ''.join(f.readlines())
        refKeybyt = bytes(refKey, 'utf-8')

# use the key and encrypt pwd
    keytouse = Fernet(refKeybyt)
    myPass = (keytouse.decrypt(encpwdbyt))

    pwd_dec=myPass.decode(encoding='utf=8')
    return pwd_dec


#Decrypt Credentials that need to be used in API
usr=decrypt_user()
pwd=decrypt_pwd()

print(usr)



