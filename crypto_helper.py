from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

import keyring
from api.conf import PEPPER, SERVICE_NAME, SALT_N, SALT_P, SALT_R, SALT_LENGTH
import base64
import os

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

#Passphrase should arrive pre-peppered
def add_salt(passphrase):
    salt = os.urandom(16)
    salt_64 = base64.b64encode(salt)
    TEMP_SALT = salt_64.decode('ascii')
    #print(f"Salt is {TEMP_SALT}")
    passphrase_bytes = bytes(passphrase, "utf-8")
    kdf = Scrypt(salt=salt, length=SALT_LENGTH, n=SALT_N, r=SALT_R, p=SALT_P)
    #Hash the passphrase
    hashed_passphrase = kdf.derive(passphrase_bytes)
    hashed_passphrase_base64 = base64.b64encode(hashed_passphrase)
    #Need peppered passphrase and salt returned
    return [hashed_passphrase_base64.decode('ascii'),TEMP_SALT]

def re_season(passphrase,salt):
    salt_64 = salt
    TEMP_SALT = base64.b64decode(salt_64)
    #print(f"Salt is {TEMP_SALT}")
    passphrase_bytes = bytes(passphrase, "utf-8")
    kdf = Scrypt(salt=TEMP_SALT, length=SALT_LENGTH, n=SALT_N, r=SALT_R, p=SALT_P)
    #Hash the passphrase
    hashed_passphrase = kdf.derive(passphrase_bytes)
    hashed_passphrase_base64 = base64.b64encode(hashed_passphrase)
    #Need peppered passphrase and salt returned
    return hashed_passphrase_base64.decode('ascii')
