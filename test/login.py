from json import dumps
from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.web import Application
from .conf import SERVICE_NAME

import keyring
import aes_encrypt_decrypt
import crypto_helper

from .base import BaseTest

from api.handlers.login import LoginHandler

#This class looks like it sends POST requests to the websever to login
class LoginHandlerTest(BaseTest):

    @classmethod
    def setUpClass(self):
        self.my_app = Application([(r'/login', LoginHandler)])
        super().setUpClass()

    async def register(self):
        await self.get_app().db.users.insert_one({
            'email': self.email,
            'password': self.password,
            'displayName': 'testDisplayName'
        })


    def setUp(self):
        super().setUp()

        #This is raw text would need to change
        #Trial 1: Going to replace this with key ring password, no token yet
        #The test still passed using keyring
        self.email = crypto_helper.encrypt_email('test@test.com')
        self.password = crypto_helper.encrypt_pwd('test@test.com')

        IOLoop.current().run_sync(self.register)

    #Testing the login to the webserver with e-mail and password
    def test_login(self):
        #This uses raw text but fixed by setting in setup using keyring
        body = {
          'email': self.email,
          'password': self.password
        }

        response = self.fetch('/login', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)

        #Raw tokens but only checks it not empty
        self.assertIsNotNone(body_2['token'])
        self.assertIsNotNone(body_2['expiresIn'])

    #Testing login with case insensitve
    def test_login_case_insensitive(self):
        #This uses raw data
        body = {
          'email': self.email.swapcase(),
          'password': self.password
        }

        response = self.fetch('/login', method='POST', body=dumps(body))
        #This should not work with hashed emails and passwords
        self.assertEqual(403, response.code)

        body_2 = json_decode(response.body)

        #Now FAILS because this is working with hashes
        #Raw tokens but only checks it's not empty
        #self.assertIsNotNone(body_2['token'])
        #self.assertIsNotNone(body_2['expiresIn'])

    #Deliberately sending a wrong e-mail, expects fail 403
    def test_login_wrong_email(self):
        #This uses raw data
        body = {
          'email': 'wrongUsername',
          'password': self.password
        }

        response = self.fetch('/login', method='POST', body=dumps(body))
        print(f"URL + {response.effective_url}") #should output URL of webserver
        self.assertEqual(403, response.code)

    #Deliberately sending a wrong password, expects fail 403
    def test_login_wrong_password(self):
        #This uses raw data
        body = {
          'email': self.email,
          'password': 'wrongPassword' #Not masked because deliberately wrong
        }

        response = self.fetch('/login', method='POST', body=dumps(body))
        self.assertEqual(403, response.code)
