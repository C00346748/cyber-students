from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import keyring

#block_size = 16

padder = padding.PKCS7(algorithms.AES.block_size).padder()
unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
ENC_KEY = os.urandom(16)
ENC_IV = os.urandom(16)

def encrypt(P):
    #key = 128 bit (16 bytes) key
    #iv, initializaion vector passed
    #P plaintext passed
    P_bytes = bytes(P, "utf-8")
    P_pad_bytes = padder.update(P_bytes) + padder.finalize() #Pad it and finalize here
    cipher = Cipher(algorithms.AES(ENC_KEY), modes.CBC(ENC_IV))
    encryptor =  cipher.encryptor()
    C = encryptor.update(P_pad_bytes) + encryptor.finalize()
    return C

def decrypt(C):
    cipher = Cipher(algorithms.AES(ENC_KEY), modes.CBC(ENC_IV))
    decryptor = cipher.decryptor()
    P_padded = decryptor.update(C) + decryptor.finalize()
    P = unpadder.update(P_padded) + unpadder.finalize() #unpad it and finalize here
    return P
    
