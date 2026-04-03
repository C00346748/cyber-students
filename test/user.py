from json import dumps
from tornado.escape import json_decode
from tornado.httputil import HTTPHeaders
from tornado.ioloop import IOLoop
from tornado.web import Application
from .conf import SERVICE_NAME, PRV_KEY, PUB_KEY
from cryptography.hazmat.primitives import hashes, serialization

import keyring
import aes_encrypt_decrypt
import rsa_encrypt_decrypt_with_keyring_chunking

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
        print(f"Set user: {self.email}") #Some prints to verify functions
        #print(f"Set user: {self.password}")
        #print(f"Set user: {self.display_name}")
        
        print('Hash**')
        plain_text = b'testing 123'
        public_key_str = PUB_KEY
        public_key = rsa_encrypt_decrypt_with_keyring_chunking.convert_pub_to_pem(public_key_str)
        cipher_text = rsa_encrypt_decrypt_with_keyring_chunking.encrypt_message(public_key, plain_text, 32)
        print("Ciphertext Hash: " + b"".join(cipher_text).hex())
        print(hash)
        private_key_str = PRV_KEY
        private_key = rsa_encrypt_decrypt_with_keyring_chunking.convert_prv_to_pem(private_key_str)
        decoded_plaintext = rsa_encrypt_decrypt_with_keyring_chunking.decrypt_message(private_key,cipher_text)
        print(f"This is decoded hash: {decoded_plaintext.decode("utf-8")}")
        '''
        #TEST
        if(PRV_KEY!=''):
            print('*** PRV PRINT ***')
            private_key_str = PRV_KEY.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
            )
            print(private_key_str.decode("utf-8"))
        #print(rsa_hash_small_message.decrypt_hash(hash))
        #print('***Hash')
        '''
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
        #password = aes_encrypt_decrypt.decrypt(self.email).decode("utf-8")
        #keyring should be added here add tokens
        self.email = 'test@test.com'
        self.password = keyring.get_password(SERVICE_NAME,self.email)
        self.display_name = 'testDisplayName'
        self.token = 'testToken'

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
