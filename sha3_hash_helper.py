from cryptography.hazmat.primitives import hashes
import keyring
import codecs
import base64

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

    print(password)

def hash(str):
    digest = hashes.Hash(hashes.SHA3_256())
    message = str.encode('utf-8') #change to bytes
    digest.update(message)
    hash_message = digest.finalize()
    message_base64 = base64.b64encode(hash_message)
    return  message_base64.decode('ascii') #return the hash


#Configure to run as script
if __name__ == '__main__':
    test_sha3()