from json import dumps
from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.web import Application
from .conf import SERVICE_NAME

import keyring
import aes_encrypt_decrypt

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
        display_name = 'testDisplayName'
        password = keyring.get_password(SERVICE_NAME,email)
        #body dictionary replacing password retrieval with keyring
        body = {
          'email': email,
          'password': password,
          'displayName': display_name
        }
        print(f"**** + {body['email']}")

        response = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)
        self.assertEqual(email, body_2['email'])
        self.assertEqual(display_name, body_2['displayName'])

    #Sends reg request without display name which is fine
    def test_registration_without_display_name(self):
        email = 'test@test.com'
        #body dictionary replacing password retrieval with keyring
        body = {
          'email': email,
          'password': keyring.get_password(SERVICE_NAME,email)
        }

        response = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)
        self.assertEqual(email, body_2['email'])
        self.assertEqual(email, body_2['displayName'])

    #Double reg, should pass first attempt and fail second attempt to reg same user
    def test_registration_twice(self):
        #body dictionary replacing password retrieval with keyring
        body = {
          'email': 'test@test.com',
          'password': keyring.get_password(SERVICE_NAME,'test@test.com'),
          'displayName': 'testDisplayName'
        }

        response = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        response_2 = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(409, response_2.code)
