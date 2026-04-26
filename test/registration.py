from json import dumps
from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.web import Application
from .conf import SERVICE_NAME

import keyring
import aes_encrypt_decrypt
import crypto_helper
import os

from api.handlers.registration import RegistrationHandler

from .base import BaseTest

import urllib.parse

#Test the registration with the webserver
class RegistrationHandlerTest(BaseTest):

    #Sets registration function to my_app, add reg handler
    @classmethod
    def setUpClass(self):
        self.my_app = Application([(r'/registration', RegistrationHandler)])
        super().setUpClass()

    #Sends reg request to webserver
    def test_registration(self):
        #print(f"Salt for user:  {crypto_helper.get_salt('test@test.com')}")
        email = crypto_helper.simple_hash('test@test.com')
        iv_email_bytes = crypto_helper.gen_16_iv()
        iv_email = crypto_helper.get_iv_string(iv_email_bytes)
        email_enc = aes_encrypt_decrypt.encrypt_aes_string_pass_iv('test@test.com',iv_email)

        #Add IV later
        display_name = 'testDisplayName'
        iv_displayName_bytes = crypto_helper.gen_16_iv()
        iv_displayName = crypto_helper.get_iv_string(iv_displayName_bytes)
        display_name = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(display_name,iv_displayName)

        #print(f"Salt and peppered display name {display_name}")
        list = crypto_helper.add_salt(crypto_helper.add_pepper('testPassword'))
        password = list[0]
        salt = list[1]
        #print(f"**** Password and Email Reg ****  {email} password {password}")
        #body dictionary replacing password retrieval with keyring

        fullname = 'testFullname'
        iv_fullname_bytes = crypto_helper.gen_16_iv()
        iv_fullname = crypto_helper.get_iv_string(iv_fullname_bytes)
        fullname = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(fullname,iv_fullname)

        address = 'testAddress'
        iv_address_bytes = crypto_helper.gen_16_iv()
        iv_address = crypto_helper.get_iv_string(iv_address_bytes)
        address = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(address,iv_address)
     
        dob = 'testDob'
        iv_dob_bytes = crypto_helper.gen_16_iv()
        iv_dob = crypto_helper.get_iv_string(iv_dob_bytes)
        dob = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(dob,iv_dob)

        phone_number = 'testPhoneNumber'
        iv_phone_number_bytes = crypto_helper.gen_16_iv()
        iv_phone_number = crypto_helper.get_iv_string(iv_phone_number_bytes)
        phone_number = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(phone_number,iv_phone_number)

        list_disabilities = 'testListDisabilities'
        iv_list_disabilities_bytes = crypto_helper.gen_16_iv()
        iv_list_disabilities = crypto_helper.get_iv_string(iv_list_disabilities_bytes)
        list_disabilities = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(list_disabilities,iv_list_disabilities)


        body = {
            'email': email,
            'email_enc': email_enc,
            'iv_email': iv_email,
            'password': password,
            'salt':salt,
            'displayName': display_name,
            'iv_displayName': iv_displayName,
            'fullname' : fullname,
            'iv_fullname': iv_fullname,
            'address': address,
            'iv_address': iv_address,
            'dob': dob,
            'iv_dob': iv_dob,
            'phone_number': phone_number,
            'iv_phone_number': iv_phone_number,
            'list_disabilities': list_disabilities,
            'iv_list_disabilities': iv_list_disabilities
        }
        #print(f"**** {body['email']}")

        response = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)
        self.assertEqual(email, body_2['email'])
        self.assertEqual(display_name, body_2['displayName'])

    #Sends reg request without display name which is fine

    def test_registration_without_display_name(self):
        email = crypto_helper.simple_hash('test@test.com')
        iv_email_bytes = crypto_helper.gen_16_iv()
        iv_email = crypto_helper.get_iv_string(iv_email_bytes)
        email_enc = aes_encrypt_decrypt.encrypt_aes_string_pass_iv('test@test.com',iv_email)

        #print(f"Salt and peppered display name {display_name}")
        list = crypto_helper.add_salt(crypto_helper.add_pepper('testPassword'))
        password = list[0]
        salt = list[1]
        #print(f"**** Password and Email Reg ****  {email} password {password}")
        #body dictionary replacing password retrieval with keyring

        fullname = 'testFullname'
        iv_fullname_bytes = crypto_helper.gen_16_iv()
        iv_fullname = crypto_helper.get_iv_string(iv_fullname_bytes)
        fullname = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(fullname,iv_fullname)

        address = 'testAddress'
        iv_address_bytes = crypto_helper.gen_16_iv()
        iv_address = crypto_helper.get_iv_string(iv_address_bytes)
        address = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(address,iv_address)
     
        dob = 'testDob'
        iv_dob_bytes = crypto_helper.gen_16_iv()
        iv_dob = crypto_helper.get_iv_string(iv_dob_bytes)
        dob = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(dob,iv_dob)

        phone_number = 'testPhoneNumber'
        iv_phone_number_bytes = crypto_helper.gen_16_iv()
        iv_phone_number = crypto_helper.get_iv_string(iv_phone_number_bytes)
        phone_number = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(phone_number,iv_phone_number)

        list_disabilities = 'testListDisabilities'
        iv_list_disabilities_bytes = crypto_helper.gen_16_iv()
        iv_list_disabilities = crypto_helper.get_iv_string(iv_list_disabilities_bytes)
        list_disabilities = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(list_disabilities,iv_list_disabilities)

        body = {
            'email': email,
            'email_enc': email_enc,
            'iv_email': iv_email,
            'password': password,
            'salt':salt,
            'fullname' : fullname,
            'iv_fullname': iv_fullname,
            'address': address,
            'iv_address': iv_address,
            'dob': dob,
            'iv_dob': iv_dob,
            'phone_number': phone_number,
            'iv_phone_number': iv_phone_number,
            'list_disabilities': list_disabilities,
            'iv_list_disabilities': iv_list_disabilities
        }

        response = self.fetch('/registration', method='POST', body=dumps(body))
        
        self.assertEqual(200, response.code)
        
        body_2 = json_decode(response.body)
        #print("Compare " + email + " with " + body_2['email'])
        self.assertEqual(email, body_2['email'])
        
        #self.assertEqual(email, body_2['displayName'])

    #Double reg, should pass first attempt and fail second attempt to reg same user
    def test_registration_twice(self):
        email = crypto_helper.simple_hash('test@test.com')
        iv_email_bytes = crypto_helper.gen_16_iv()
        iv_email = crypto_helper.get_iv_string(iv_email_bytes)
        email_enc = aes_encrypt_decrypt.encrypt_aes_string_pass_iv('test@test.com',iv_email)

        #Add IV later
        display_name = 'testDisplayName'
        iv_displayName_bytes = crypto_helper.gen_16_iv()
        iv_displayName = crypto_helper.get_iv_string(iv_displayName_bytes)
        display_name = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(display_name,iv_displayName)

        #print(f"Salt and peppered display name {display_name}")
        list = crypto_helper.add_salt(crypto_helper.add_pepper('testPassword'))
        password = list[0]
        salt = list[1]
        #print(f"**** Password and Email Reg ****  {email} password {password}")
        #body dictionary replacing password retrieval with keyring

        fullname = 'testFullname'
        iv_fullname_bytes = crypto_helper.gen_16_iv()
        iv_fullname = crypto_helper.get_iv_string(iv_fullname_bytes)
        fullname = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(fullname,iv_fullname)

        address = 'testAddress'
        iv_address_bytes = crypto_helper.gen_16_iv()
        iv_address = crypto_helper.get_iv_string(iv_address_bytes)
        address = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(address,iv_address)
     
        dob = 'testDob'
        iv_dob_bytes = crypto_helper.gen_16_iv()
        iv_dob = crypto_helper.get_iv_string(iv_dob_bytes)
        dob = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(dob,iv_dob)

        phone_number = 'testPhoneNumber'
        iv_phone_number_bytes = crypto_helper.gen_16_iv()
        iv_phone_number = crypto_helper.get_iv_string(iv_phone_number_bytes)
        phone_number = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(phone_number,iv_phone_number)

        list_disabilities = 'testListDisabilities'
        iv_list_disabilities_bytes = crypto_helper.gen_16_iv()
        iv_list_disabilities = crypto_helper.get_iv_string(iv_list_disabilities_bytes)
        list_disabilities = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(list_disabilities,iv_list_disabilities)


        body = {
            'email': email,
            'email_enc': email_enc,
            'iv_email': iv_email,
            'password': password,
            'salt':salt,
            'displayName': display_name,
            'iv_displayName': iv_displayName,
            'fullname' : fullname,
            'iv_fullname': iv_fullname,
            'address': address,
            'iv_address': iv_address,
            'dob': dob,
            'iv_dob': iv_dob,
            'phone_number': phone_number,
            'iv_phone_number': iv_phone_number,
            'list_disabilities': list_disabilities,
            'iv_list_disabilities': iv_list_disabilities
        }
        #print(f"**** {body['email']}")

        response = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        response_2 = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(409, response_2.code)

    #Sends reg request without display name which is fine


        