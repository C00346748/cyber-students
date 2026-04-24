from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

import keyring
from api.conf import PEPPER, SERVICE_NAME, TEMP_SALT
import base64
import os

#SHA3 was considered but probably overkill
def test_sha3():
    digest = hashes.Hash(hashes.SHA3_256())
    message = b"test@test.com"
    digest.update(message)
    hash_message = digest.finalize()
    hash_message_hex = hash_message.hex()
    print(f"Hex is: {hash_message_hex}")
    email_base64 = base64.b64encode(hash_message)
    print(f"Base 64 is : {email_base64.decode('ascii')}")
    password = keyring.get_password("key_db",email_base64.decode('ascii'))
    print("Password: " + password)

def hash(str):
    digest = hashes.Hash(hashes.SHA3_256())
    message = str.encode('utf-8') #change to bytes
    digest.update(message)
    hash_message = digest.finalize()
    message_base64 = base64.b64encode(hash_message)
    return  message_base64.decode('ascii') #return the hash in ascii

#Pepper passed str, return string, using HMAC (Hash-based Message authentication)
def add_pepper(str):
    #bytes
    message = str.encode('utf-8')
    #Hash-based Message Authentication Code
    hash_message = hmac.HMAC(PEPPER.encode('utf-8'), hashes.SHA256(), backend=default_backend())
    hash_message.update(message)
    hash_bytes = hash_message.finalize()
    hash_b64 = base64.b64encode(hash_bytes)
    # Return the peppered string
    return hash_b64.decode('ascii')

#To use this you need to pass the salt associated with user
def add_salt_and_pepper(str,salt):
    salt_64 = base64.b64encode(salt.encode())
    salted_and_peppered = salt_64.decode('ascii') + hash(str) + add_pepper(str)
    return salted_and_peppered

#Passphrase should arrive pre-peppered
def add_salt(passphrase):
    salt = os.urandom(16)
    TEMP_SALT = salt.decode('utf-8')
    print(f"Salt is {TEMP_SALT}")
    passphrase_bytes = bytes(passphrase, "utf-8")
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    #Hash the passphrase
    hashed_passphrase = kdf.derive(passphrase_bytes)
    return hashed_passphrase
    
def set_salt(user):
    #Will be sent to the database
    base64_rand = base64.b64encode(os.urandom(32))
    rand_str = base64_rand.decode('utf-8')
    if(get_salt(user)==None):
        keyring.set_password("salts",user,rand_str)

def get_salt(user):
    try:
        return keyring.get_password("salts",user)
    except:
        return None
    
def set_token():
    return None

def encrypt_pwd(user_email):
    set_salt(user_email) #only done if not done already per user email
    email = add_salt_and_pepper(user_email,get_salt(user_email))
    password = add_salt_and_pepper(keyring.get_password(SERVICE_NAME,hash('test@test.com')),get_salt(user_email))
    return password

def encrypt_pwd_new(password,user_email):
    set_salt(user_email) #only done if not done already per user email
    password = add_salt_and_pepper(password,get_salt(user_email))
    return password

def encrypt_email(user_email):
    set_salt(user_email) #only done if not done already per user email
    email = add_salt_and_pepper(user_email,get_salt(user_email))
    return email

def encrypt_other_string(user_mail, str_to_encrypt):
    return add_salt_and_pepper(str_to_encrypt,get_salt(user_mail))

#Configure to run as script
if __name__ == '__main__':
    test_sha3()
    print("Peppered: " + add_pepper('test@test.com'))
    print("Salted and Peppered: " + add_salt_and_pepper('test@test.com'))