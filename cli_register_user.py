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
import base64
import input_helper

from api.handlers.registration import RegistrationHandler
from email_validator import validate_email, EmailNotValidError

import urllib.parse


#Sends reg request to webserver
async def cli_registration():
    tracemalloc.start()
    print(f"*** Calling reg ***:")
    #Because the e-mail is not needed again I am hashing it
    #If the e-mail was needed again I would encrypt it but then I'd need iv to match to DB
    email_sentinel = True
    while(email_sentinel):
        email_in = input('Please enter your email: ')
        if(input_helper.verifyEmail(email_in)):
            email_sentinel = False
        else:
            print("Bad email format try again")
            email_sentinel = True
    #All input would need to be validated, e.g., password length and patterns
    email = crypto_helper.simple_hash(email_in)
    password_sentinel = True
    while(password_sentinel):
        password_in = pwinput.pwinput('Enter your password: ')
        if(input_helper.verifyPasswordLengthOnly(password_in)):
            password_sentinel = False
        else:
            print(f"Password must be more than {input_helper.MIN_PASSWORD_LENGTH} characters, at least one number, at least one upper case")
            password_sentinel = True
    list = crypto_helper.add_salt(crypto_helper.add_pepper(password_in))
    password = list[0]
    salt = list[1]
    display_name = aes_encrypt_decrypt.encrypt_aes_string(input('Enter the display name to use: '))
    #Get the IV for later decryptions from displayname entry
    iv = aes_encrypt_decrypt.extract_iv_string(display_name)
    fullname = aes_encrypt_decrypt.encrypt_aes_string(input('Enter your full name: '))
    address = aes_encrypt_decrypt.encrypt_aes_string(input('Enter your full address: '))
    dob = aes_encrypt_decrypt.encrypt_aes_string(input('Enter your date of birth DD/MM/YYYY: ')) 
    phone_number = aes_encrypt_decrypt.encrypt_aes_string(input('Enter your phone number: '))
    list_disabilities = aes_encrypt_decrypt.encrypt_aes_string(input('Enter your list of disabilities: '))

    print("CLI REG *** " + salt + " passphrase " + password)
    #print(f"**** Password and Email Reg ****  {email} password {password}")
    #body dictionary replacing password retrieval with keyring

    body = {
        'email': email,
        'iv': iv,
        'password': password,
        'salt':salt,
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

