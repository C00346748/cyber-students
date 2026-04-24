from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import keyring
import base64

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
    cipher = Cipher(algorithms.AES(ENC_KEY), modes.CBC(ENC_IV), backend=default_backend())
    encryptor =  cipher.encryptor()
    C_bytes = encryptor.update(P_pad_bytes) #+ encryptor.finalize()
    C_base64 = base64.b64encode(C_bytes)
    return C_base64.decode('ascii')

def decrypt(C):
    cipher = Cipher(algorithms.AES(ENC_KEY), modes.CBC(ENC_IV), backend=default_backend())
    C_bytes = bytes(C, "utf-8")
    decryptor = cipher.decryptor()
    P_padded = decryptor.update(C_bytes) + decryptor.finalize()
    P = unpadder.update(P_padded) + unpadder.finalize() #unpad it and finalize here
    P_base64 = base64.b64encode(P)
    return P_base64.decode('ascii')

def encrypt_aes(data):
    # Padding: AES-128 requires 128-bit blocks
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(ENC_KEY), modes.CBC(ENC_IV), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(padded_data) + encryptor.finalize()

def decrypt_aes(ciphertext):
    cipher = Cipher(algorithms.AES(ENC_KEY), modes.CBC(ENC_IV), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()

def encrypt_aes_string(data):
    # Padding: AES-128 requires 128-bit blocks
    data_bytes = bytes(data, "utf-8") #decode to bytes
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data_bytes) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(ENC_KEY), modes.CBC(ENC_IV), backend=default_backend())
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    data_64 = base64.b64encode(cipher_text)

    return data_64.decode('utf-8') #return string version of base 64

def decrypt_aes_string(ciphertext):

    #from string to 64 base bytes
    ciphertext_64_bytes = ciphertext.encode('ascii')
    #Decode to string bytes
    cipherbytes = base64.b64decode(ciphertext_64_bytes)

    cipher = Cipher(algorithms.AES(ENC_KEY), modes.CBC(ENC_IV), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(cipherbytes) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()

    plain_bytes = unpadder.update(padded_data) + unpadder.finalize()
    #Gave back plain bytes...converting to base 64
    plain_64 = base64.b64encode(plain_bytes)
    #Converting the base 64 to base 64 string
    plain_text = plain_64.decode('ascii')
    #change the base 64 string to acsii string for return
    plain_string = base64.b64decode(plain_text).decode('utf-8')

    return plain_string

if __name__ == '__main__':
    '''
    string = b'luke'
    enc = encrypt_aes(string)
    enc_64=base64.b64encode(enc)
    print("Enc: " + enc_64.decode("utf-8"))
    enc=base64.b64decode(enc_64)
    dec = decrypt_aes(enc)
    print("Dec: " + dec.decode("utf-8"))
    '''

    string2 = 'luke'
    enc2 = encrypt_aes_string(string2)
    #enc2_64=base64.b64encode(enc)
    print("Enc: " + enc2)
    #enc2=base64.b64decode(enc2_64)
    dec2 = decrypt_aes_string(enc2)
    print("Dec: " + dec2)

    
