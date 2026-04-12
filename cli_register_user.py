from json import dumps
from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.web import Application
from api.conf import SERVICE_NAME, MONGODB_DBNAME, WORKERS, MONGODB_HOST, BASE_URL
from tornado.testing import AsyncHTTPTestCase
from motor.motor_tornado import MotorClient

from concurrent.futures import ThreadPoolExecutor
from mongomock_motor import AsyncMongoMockClient
from tornado.httpclient import AsyncHTTPClient

import keyring
import aes_encrypt_decrypt
import crypto_helper
import asyncio
import tracemalloc
import pwinput

from api.handlers.registration import RegistrationHandler

import urllib.parse


#Sends reg request to webserver
async def cli_registration():
    tracemalloc.start()
    print(f"*** Calling reg ***:")
    email_in = input('Please enter your email: ')
    password_in = pwinput.pwinput('Enter your password: ')
    display_name_in = input('Enter the display name to use: ')
    full_name_in = input('Enter your full name: ')
    address_in = input('Enter your full address: ')
    dob_in = input('Enter your date of birth DD/MM/YYY: ')
    phone_number_in = input('Enter your phone number: ')
    list_disabilities_in = input('Enter your list of disabilities: ')



    #my_app = Application([(r'/registration', RegistrationHandler)])
    
    #my_app.db = AsyncMongoMockClient()[MONGODB_DBNAME]
    #my_app.executor = ThreadPoolExecutor(WORKERS)
    
    email = crypto_helper.encrypt_email(email_in)
    display_name = crypto_helper.encrypt_other_string(email_in,display_name_in)
    #print(f"Salt and peppered display name {display_name}")
    password = crypto_helper.encrypt_pwd_new(password_in,email_in)
    #print(f"**** Password and Email Reg ****  {email} password {password}")
    #body dictionary replacing password retrieval with keyring
    fullname = crypto_helper.encrypt_other_string(email_in,full_name_in)
    address = crypto_helper.encrypt_other_string(email_in,address_in)
    dob = crypto_helper.encrypt_other_string(email_in,dob_in)
    phone_number = crypto_helper.encrypt_other_string(email_in,phone_number_in)
    list_disabilities = crypto_helper.encrypt_other_string(email_in,list_disabilities_in)

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
    http_client = AsyncHTTPClient()
    url = BASE_URL + "api/registration"
    #Send request to registration handler
    #response = my_app.start_request('/registration', method='POST', body=dumps(body))
    
    response = await http_client.fetch(
        url,
        method="POST",
        body=dumps(body),
        headers={"Content-Type": "application/json"}
    )
    print(f"Server response {response.code}")
    

async def welcome():
    http_client = AsyncHTTPClient()
    url = BASE_URL + "api/"
    #Send request to registration handler
    #response = my_app.start_request('/registration', method='POST', body=dumps(body))
    
    response = await http_client.fetch(
        url,
        method="GET"
    )

    body = json_decode(response.body)
    print(body['message'])

    #Configure to run as script
if __name__ == '__main__':
    asyncio.run(welcome())
    asyncio.run(cli_registration())

