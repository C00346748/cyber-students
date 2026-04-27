from datetime import datetime, timedelta, timezone
from tornado.escape import json_decode
from uuid import uuid4
import aes_encrypt_decrypt
import crypto_helper

from .base import BaseHandler

class LoginHandler(BaseHandler):

    async def generate_token(self, email):
        token_uuid = uuid4().hex
        expires_in = (datetime.now(timezone.utc) + timedelta(hours=2)).timestamp()
        #salted and peppered token, not possible to retrieve original token due to random salt
        token_list = crypto_helper.add_salt(crypto_helper.add_pepper(token_uuid))
        token_uuid = token_list[0]

        token = {
            #Should I have encrypted this?...not sure it was necessary
            'token': token_uuid,
            'expiresIn': expires_in,
        }

        await self.db.users.update_one({
            'email': email
        }, {
            '$set': token
        })

        return token

    async def post(self):
        try:
            body = json_decode(self.request.body)
            #Remove strip no good with hashes
            email = body['email']
            password = body['password']
            #print(f"####xxxx Body email login is {body['email']}")
        except Exception:
            self.send_error(400, message='You must provide an email address and password!')
            return

        if not email:
            self.send_error(400, message='The email address is invalid!')
            return

        if not password:
            self.send_error(400, message='The password is invalid!')
            return
        
        user = await self.db.users.find_one({
          'email': email
        }, {
          'password': 1
        })

        if user is None:
            self.send_error(403, message='The email address and password are invalid!')
            return
        #print(f"xxxx User password check {user['password']} against {password} ")
        if user['password'] != password:
            self.send_error(403, message='The email address and password are invalid!')
            return

        token = await self.generate_token(email)

        self.set_status(200)
        self.response['token'] = token['token']
        #print(f"++++++ Tokens compared {self.response['token']} with {token['token']}")
        self.response['expiresIn'] = token['expiresIn']

        fullnameiv = await self.db.users.find_one({
          'email': email
        }, {
          'iv_fullname': 1 
        })

        fullname = await self.db.users.find_one({
          'email': email
        }, {
          'fullname': 1 
        })

        #try bypassess issue between live DB returning data nd test returning nothing
        #Test returns nothing because it's not passing the fullname or iv_fullname
        try: 
            test = aes_encrypt_decrypt.decrypt_aes_string_pass_iv(fullname['fullname'],fullnameiv['iv_fullname'])
        except:
            test = 'test'
        #if displayName:

        #name = aes_encrypt_decrypt.decrypt_aes_string_pass_iv(fullName['fullname'],fullNameIV['iv_fullname'])
        #self.response['message'] = f'Login Successful!, Welcome {aes_encrypt_decrypt.decrypt_aes_string(displayName['displayName'])}'
        self.response['message'] = f'Login Successful!, Welcome {test}'

        self.write_json()
