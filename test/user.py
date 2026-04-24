from json import dumps
from tornado.escape import json_decode
from tornado.httputil import HTTPHeaders
from tornado.ioloop import IOLoop
from tornado.web import Application
from .conf import SERVICE_NAME, PRV_KEY, PUB_KEY
from cryptography.hazmat.primitives import hashes, serialization

import keyring
import aes_encrypt_decrypt
import crypto_helper
import base64

from api.handlers.user import UserHandler

from .base import BaseTest

#Set and get users from DB via Webserver
class UserHandlerTest(BaseTest):

    #Testing user call to webserver, seems to be seting up a user via the db through webserver
    @classmethod
    def setUpClass(self):
        self.my_app = Application([(r'/user', UserHandler)])
        super().setUpClass()

    #Sets a user
    async def register(self):
        await self.get_app().db.users.insert_one({
            'email': self.email,
            'password': self.password,
            'displayName': self.display_name
        })
        #print(f"Set user: {self.email}") #Some prints to verify functions
        #print(f"Password user: {self.password}") #Some prints to verify functions
        #print(f"Display Name: {self.display_name}") #Some prints to verify functions
         
        #print(f"Set user: {self.password}")
        #print(f"Set user: {self.display_name}")
        
        #print('Hash**')

    #Gets the database connection via webserver and calls update
    #Setting token on the user
    async def login(self):
        await self.get_app().db.users.update_one({
            'email': self.email
        }, {
            '$set': { 'token': self.token, 'expiresIn': 2147483647 }
        })

    #Sets up user and calls proc to register and login
    def setUp(self):
        super().setUp()

        self.email = aes_encrypt_decrypt.encrypt_aes_string('test@test.com')
        
        list = crypto_helper.add_salt(crypto_helper.add_pepper('testPassword'))
        salt = list[1] #Not using salt yet
        self.password = list[0]
        self.display_name = aes_encrypt_decrypt.encrypt_aes_string('testDisplayName')
        self.token = aes_encrypt_decrypt.encrypt_aes_string('testToken')

        IOLoop.current().run_sync(self.register)
        IOLoop.current().run_sync(self.login)

    #Fetch user with token
    def test_user(self):
        headers = HTTPHeaders({'X-Token': self.token})

        response = self.fetch('/user', headers=headers)
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)
        self.assertEqual(self.email, body_2['email'])
        self.assertEqual(self.display_name, body_2['displayName'])

    #Fetch attempt without token, expect fails
    def test_user_without_token(self):
        response = self.fetch('/user')
        self.assertEqual(400, response.code)

    #Fetch attempt without token, expect fails
    def test_user_wrong_token(self):
        headers = HTTPHeaders({'X-Token': 'wrongToken'})

        response = self.fetch('/user')
        self.assertEqual(400, response.code)
