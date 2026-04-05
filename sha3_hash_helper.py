from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
import keyring
from test.conf import PEPPER
import base64
import os

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

def add_pepper(str):
    message = str.encode('utf-8')
    #Hash-based Message Authentication Code
    hash_message = hmac.HMAC(PEPPER.encode('utf-8'), hashes.SHA3_256(), backend=default_backend())
    hash_message.update(message)
    hash_bytes = hash_message.finalize()
    hash_b64 = base64.b64encode(hash_bytes)
    # Return the peppered password as bytes for the next hashing step
    return hash_b64.decode('ascii')

def add_salt_and_pepper(str):
    salt = os.urandom(32) #Salt 256
    salt_64 = base64.b64encode(salt)
    salted_and_peppered = salt_64.decode('ascii') + hash(str) + add_pepper(str)
    return salted_and_peppered

#Configure to run as script
if __name__ == '__main__':
    test_sha3()
    print("Peppered: " + add_pepper('test@test.com'))
    print("Salted and Peppered: " + add_salt_and_pepper('test@test.com'))