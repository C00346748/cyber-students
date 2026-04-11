from json import dumps
from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.web import Application
from test.conf import SERVICE_NAME, MONGODB_DBNAME, WORKERS
from tornado.testing import AsyncHTTPTestCase

from concurrent.futures import ThreadPoolExecutor
from mongomock_motor import AsyncMongoMockClient
from tornado.httpclient import AsyncHTTPClient

import keyring
import aes_encrypt_decrypt
import crypto_helper
import asyncio

from api.handlers.registration import RegistrationHandler

import urllib.parse


#A limited amount of input, this time not using command line
async def limited_data():
    email = input('Please enter your email')
    password = input('Enter your password: ')
    displayName = input('Enter the display name to use')
    crypto_helper.set_salt(email)
    registration(email,password,displayName)

#Sends reg request to webserver
async def registration(email_in,password_in,display_name_in):
    my_app = Application([(r'/registration', RegistrationHandler)])
    print(f"The app is:  {my_app}")
    my_app.db = AsyncMongoMockClient()[MONGODB_DBNAME]
    my_app.executor = ThreadPoolExecutor(WORKERS)
    
    email = crypto_helper.encrypt_email(email_in)
    display_name = crypto_helper.encrypt_other_string(email_in,display_name_in)
    #print(f"Salt and peppered display name {display_name}")
    password = crypto_helper.encrypt_pwd(email_in)
    #print(f"**** Password and Email Reg ****  {email} password {password}")
    #body dictionary replacing password retrieval with keyring
    body = {
        'email': email,
        'password': password,
        'displayName': display_name
    }
    #print(f"**** {body['email']}")
    http_client = AsyncHTTPClient()
    url = "http://localhost:4000/students/api/registration"
    #Send request to registration handler
    #response = my_app.start_request('/registration', method='POST', body=dumps(body))
    
    response = await http_client.fetch(
        url,
        method="POST",
        body=dumps(body),
        headers={"Content-Type": "application/json"}
    )
    print(f"Server response {response.code}")

    #response2 = await my_app.db.users.insert_one({
           # 'email': email,
           # 'password': password,
           # 'displayName': display_name
    #})
    
    #print("Server response " + response2.code)

    #Configure to run as script
if __name__ == '__main__':
    asyncio.run(limited_data())
