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
        #Add IV later
        display_name = aes_encrypt_decrypt.encrypt_aes_string('testDisplayName')
        iv = aes_encrypt_decrypt.extract_iv_string(display_name)
        #print(f"Salt and peppered display name {display_name}")
        list = crypto_helper.add_salt(crypto_helper.add_pepper('testPassword'))
        password = list[0]
        salt = list[1]
        #print(f"**** Password and Email Reg ****  {email} password {password}")
        #body dictionary replacing password retrieval with keyring
        fullname = aes_encrypt_decrypt.encrypt_aes_string('x')
        address = aes_encrypt_decrypt.encrypt_aes_string('x')
        dob = aes_encrypt_decrypt.encrypt_aes_string('x')
        phone_number = aes_encrypt_decrypt.encrypt_aes_string('x')
        list_disabilities = aes_encrypt_decrypt.encrypt_aes_string('x')
        body = {
          'email': email,
          'iv': iv,
          'password': password,
          'salt': salt,
          'displayName': display_name,
          'fullname' : fullname,
          'address': address,
          'dob': dob,
          'phone_number': phone_number,
          'list_disabilities': list_disabilities
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
        list = crypto_helper.add_salt(crypto_helper.add_pepper('testPassword'))
        password = list[0]
        salt = list[1]
        #print(f"**** Password and Email Reg ****  {email} password {password}")
        #body dictionary replacing password retrieval with keyring
        fullname = aes_encrypt_decrypt.encrypt_aes_string('x')
        iv = aes_encrypt_decrypt.extract_iv_string(fullname)
        address = aes_encrypt_decrypt.encrypt_aes_string('x')
        dob = aes_encrypt_decrypt.encrypt_aes_string('x')
        phone_number = aes_encrypt_decrypt.encrypt_aes_string('x')
        list_disabilities = aes_encrypt_decrypt.encrypt_aes_string('x')

        body = {
          'email': email,
          'iv': iv,
          'password': password,
          'salt':salt,
          'fullname' : fullname,
          'address': address,
          'dob': dob,
          'phone_number': phone_number,
          'list_disabilities': list_disabilities
        }

        response = self.fetch('/registration', method='POST', body=dumps(body))
        
        self.assertEqual(200, response.code)
        
        body_2 = json_decode(response.body)
        #print("Compare " + email + " with " + body_2['email'])
        self.assertEqual(email, body_2['email'])
        
        self.assertEqual(email, body_2['displayName'])

    #Double reg, should pass first attempt and fail second attempt to reg same user
    def test_registration_twice(self):
        email = crypto_helper.simple_hash('test@test.com')
        #print("Email in test without display name " + email)
        list = crypto_helper.add_salt(crypto_helper.add_pepper('testPassword'))
        password = list[0]
        salt = list[1]
        #print("Password in test without display name " + password)
        #body dictionary replacing password retrieval with keyring
        display_name = aes_encrypt_decrypt.encrypt_aes_string('testDisplayName')
        iv = aes_encrypt_decrypt.extract_iv_string(display_name)
        #print(f"**** Password and Email Reg ****  {email} password {password}")
        #body dictionary replacing password retrieval with keyring
        fullname = aes_encrypt_decrypt.encrypt_aes_string('x')
        address = aes_encrypt_decrypt.encrypt_aes_string('x')
        dob = aes_encrypt_decrypt.encrypt_aes_string('x')
        phone_number = aes_encrypt_decrypt.encrypt_aes_string('x')
        list_disabilities = aes_encrypt_decrypt.encrypt_aes_string('x')

        body = {
          'email': email,
          'iv': iv,
          'password': password,
          'salt': salt,
          'displayName': display_name,
          'fullname' : fullname,
          'address': address,
          'dob': dob,
          'phone_number': phone_number,
          'list_disabilities': list_disabilities
        }

        response = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        response_2 = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(409, response_2.code)
        