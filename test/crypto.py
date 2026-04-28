import os
import aes_encrypt_decrypt
import crypto_helper
import unittest
from .base import BaseTest
import base64
import random
import string

class CryptoTest(unittest.TestCase):
    
    #Testing encrypt with iv
    def test_aes_with_iv_roundtrip(self):
        length_of_string = random.randint(1, 100)
        string2 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        iv_bytes = crypto_helper.gen_16_iv()
        iv_string = crypto_helper.get_iv_string(iv_bytes)
        print(iv_string)
        enc2 = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(string2,iv_string)
        #enc2_64=base64.b64encode(enc2)
        print("Enc: " + enc2)
        #enc2=base64.b64decode(enc2_64)
        dec2 = aes_encrypt_decrypt.decrypt_aes_string_pass_iv(enc2,iv_string)
        print("Dec: " + dec2)
        
        self.assertEqual(string2, dec2)

    def test_hundred_strings_aes(self):
        for i in range(1, 101):
            self.test_aes_with_iv_roundtrip()

    def test_hash_same_string(self):
        length_of_string = random.randint(1, 100)
        string1 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        string2 = string1
        string1_hash = crypto_helper.simple_hash(string1)
        string2_hash = crypto_helper.simple_hash(string2)
        #same string same hash?
        self.assertEqual(string1_hash,string2_hash)

    def test_hash_different_string(self):
        length_of_string = random.randint(1, 100)
        string1 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        string2 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        if(string1 != string2):
            string1_hash = crypto_helper.simple_hash(string1)
            string2_hash = crypto_helper.simple_hash(string2)
        #different string never same hash?
        self.assertNotEqual(string1_hash,string2_hash)