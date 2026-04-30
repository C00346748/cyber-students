import os
import aes_encrypt_decrypt
import crypto_helper
import unittest
from .base import BaseTest
import base64
import random
import string
from uuid import uuid4

class CryptoTest(unittest.TestCase):
    
    #Testing encrypt with iv
    def test_aes_with_iv_roundtrip(self):
        length_of_string = random.randint(1, 100)
        string2 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        iv_bytes = crypto_helper.gen_16_iv()
        iv_string = crypto_helper.get_iv_string(iv_bytes)
        enc2 = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(string2,iv_string)
        #enc2_64=base64.b64encode(enc2)
        #enc2=base64.b64decode(enc2_64)
        dec2 = aes_encrypt_decrypt.decrypt_aes_string_pass_iv(enc2,iv_string)
        
        self.assertEqual(string2, dec2)

    #test many different string of different lengths
    def test_many_strings_aes(self):
        #Set at 100 string test
        for i in range(1, 101):
            self.test_aes_with_iv_roundtrip()

    #Test that hash of same string always produces same hash
    def test_hash_same_string(self):
        length_of_string = random.randint(1, 100)
        string1 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        string2 = string1
        string1_hash = crypto_helper.simple_hash(string1)
        string2_hash = crypto_helper.simple_hash(string2)
        #same string same hash?
        self.assertEqual(string1_hash,string2_hash)

    #Test that hash of different strings always produce different hash (no collision - shouldn't happen if coded correctly)
    def test_hash_different_string(self):
        length_of_string = random.randint(1, 100)
        string1 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        string2 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        if(string1 != string2):
            string1_hash = crypto_helper.simple_hash(string1)
            string2_hash = crypto_helper.simple_hash(string2)
            self.assertNotEqual(string1_hash,string2_hash)

    #Hashes would likely not match if there was an issue with the implementation
    def test_hash_token(self):
        #generate token
        token_uuid = uuid4().hex
        #same non-hashed value
        token2 = token_uuid
        #hash token with salt and pepper
        token_list = crypto_helper.add_salt(crypto_helper.add_pepper(token_uuid))
        token_uuid = token_list[0]
        #hash second token
        token_list2 = crypto_helper.add_salt(crypto_helper.add_pepper(token_uuid))
        token_uuid2 = token_list2[0]
        #values should be equal
        self.assertNotEqual(token_uuid,token_uuid2)

    #test many hashes of tokens
    def test_hash_multiple(self):
        #Takes a while to execute 100, so staying with 50
        for i in range (1, 50):
            self.test_hash_token()

    #if these are ever not equal then there is something wrong with the implmentation
    def test_hash_password(self):
        password1 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        password2 = password1
        #hash the password with salt and pepper
        password1_hash = crypto_helper.add_salt(crypto_helper.add_pepper(password1))
        password1_hash = password1_hash[0]
        #hash the same second password
        password2_hash = crypto_helper.add_salt(crypto_helper.add_pepper(password2))
        password2_hash = password2_hash[0]
        #values should always be equal
        self.assertNotEqual(password1_hash,password2_hash)

    #test many hashes of passwords
    def test_hash_multiple_password(self):
        #Takes a while to execute 100, so staying with 50
        for i in range (1, 50):
            self.test_hash_password()