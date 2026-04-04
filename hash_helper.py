from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend

import os
import keyring
from test.conf import SERVICE_NAME, PRV_KEY, PUB_KEY

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=1024
)

#instead bring in the private key from key ring hash_prv

private_key_str = keyring.get_password("hash_prv","None")
#Just printing in test mode
print(private_key_str)


def convert_prv_to_pem(key):
    private_key = serialization.load_pem_private_key(
        bytes(private_key_str, "utf-8"), 
        password=None,
        backend=default_backend()
    )
    return private_key

private_key = convert_prv_to_pem(private_key_str)

public_key_str = keyring.get_password("hash_pub","None")

print(public_key_str)
#import public key from keyring also
#public_key_str = keyring.get_password("hash_pub","None")
#print(public_key_str)
def convert_pub_to_pem(key):
    public_key = serialization.load_pem_public_key(
        bytes(key, "utf-8"),
        backend=default_backend()
    )
    return public_key

public_key = convert_pub_to_pem(public_key_str)

def split_message(message, chunk_size):
    return [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]

def encrypt_message(public_key, message, chunk_size):
    encrypted_chunks = []
    for chunk in split_message(message, chunk_size):
        encrypted_chunks.append(public_key.encrypt(
            chunk,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ))
    return encrypted_chunks

def decrypt_message(private_key, encrypted_chunks):
    decrypted_chunks = []
    for chunk in encrypted_chunks:
        decrypted_chunks.append(private_key.decrypt(
            chunk,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ))
    return b"".join(decrypted_chunks)

def hash_string(str):
    str_bytes = str.encode("utf-8")
    public_key_str = PUB_KEY
    public_key = convert_pub_to_pem(public_key_str)
    cipher_text = encrypt_message(public_key,str_bytes, 32)
    return cipher_text

def dehash_string(str):
    private_key_str = PRV_KEY
    private_key = convert_prv_to_pem(private_key_str)
    decoded_plaintext = decrypt_message(private_key,str)
    return decoded_plaintext.decode("utf-8")


# Test cases
'''
long_plaintext = b'This is a really  really  really  really  really  really  really  really  really  really  really  really  really  really  really  really  really  really long piece of text'
long_ciphertext = encrypt_message(public_key, long_plaintext, 32)
long_plaintext_2 = decrypt_message(private_key, long_ciphertext)

print()
print("Plaintext: " + long_plaintext.decode("utf-8"))
print()
print("Ciphertext: " + b"".join(long_ciphertext).hex())
print()
print("Original Plaintext: " + long_plaintext_2.decode("utf-8"))
'''
