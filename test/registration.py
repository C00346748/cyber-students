from json import dumps
from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.web import Application
from .conf import SERVICE_NAME

import keyring
import aes_encrypt_decrypt
import crypto_helper

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
        email = 'test@test.com'
        crypto_helper.set_salt('test@test.com')
        #print(f"Salt for user:  {crypto_helper.get_salt('test@test.com')}")
        email = crypto_helper.encrypt_email('test@test.com')
        display_name = crypto_helper.encrypt_other_string('test@test.com','testDisplayName')
        #print(f"Salt and peppered display name {display_name}")
        password = crypto_helper.encrypt_pwd('test@test.com')
        #print(f"**** Password and Email Reg ****  {email} password {password}")
        #body dictionary replacing password retrieval with keyring
        fullname = crypto_helper.encrypt_other_string('test@test.com','x')
        address = crypto_helper.encrypt_other_string('test@test.com','x')
        dob = crypto_helper.encrypt_other_string('test@test.com','x')
        phone_number = crypto_helper.encrypt_other_string('test@test.com','x')
        list_disabilities = crypto_helper.encrypt_other_string('test@test.com','x')
        body = {
          'email': email,
          'password': password,
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
        email = crypto_helper.encrypt_email('test@test.com')
        password = crypto_helper.encrypt_pwd('test@test.com')
        #print(f"**** Password and Email Reg ****  {email} password {password}")
        #body dictionary replacing password retrieval with keyring
        fullname = crypto_helper.encrypt_other_string('test@test.com','x')
        address = crypto_helper.encrypt_other_string('test@test.com','x')
        dob = crypto_helper.encrypt_other_string('test@test.com','x')
        phone_number = crypto_helper.encrypt_other_string('test@test.com','x')
        list_disabilities = crypto_helper.encrypt_other_string('test@test.com','x')

        body = {
          'email': email,
          'password': password,
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
        email = crypto_helper.add_salt_and_pepper('test@test.com',crypto_helper.get_salt('test@test.com'))
        #print("Email in test without display name " + email)
        password = crypto_helper.add_salt_and_pepper(keyring.get_password(SERVICE_NAME,crypto_helper.hash('test@test.com')),crypto_helper.get_salt('test@test.com'))
        #print("Password in test without display name " + password)
        #body dictionary replacing password retrieval with keyring
        display_name = crypto_helper.add_salt_and_pepper('testDisplayName',crypto_helper.get_salt('test@test.com'))
        password = crypto_helper.encrypt_pwd('test@test.com')
        #print(f"**** Password and Email Reg ****  {email} password {password}")
        #body dictionary replacing password retrieval with keyring
        fullname = crypto_helper.encrypt_other_string('test@test.com','x')
        address = crypto_helper.encrypt_other_string('test@test.com','x')
        dob = crypto_helper.encrypt_other_string('test@test.com','x')
        phone_number = crypto_helper.encrypt_other_string('test@test.com','x')
        list_disabilities = crypto_helper.encrypt_other_string('test@test.com','x')

        body = {
          'email': email,
          'password': password,
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
