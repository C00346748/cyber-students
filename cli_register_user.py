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
    iv_email_bytes = crypto_helper.gen_16_iv()
    iv_email = crypto_helper.get_iv_string(iv_email_bytes)
    email_enc = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(email_in,iv_email)

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

    display_name_in = input('Enter the display name to use: ')
    iv_displayName_bytes = crypto_helper.gen_16_iv()
    iv_displayName = crypto_helper.get_iv_string(iv_displayName_bytes)
    display_name = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(display_name_in,iv_displayName)

    fullname_in = input('Enter your full name: ')
    iv_fullname_bytes = crypto_helper.gen_16_iv()
    iv_fullname = crypto_helper.get_iv_string(iv_fullname_bytes)
    fullname = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(fullname_in,iv_fullname)

    address_in = input('Enter your full address: ')
    iv_address_bytes = crypto_helper.gen_16_iv()
    iv_address = crypto_helper.get_iv_string(iv_address_bytes)
    address = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(address_in,iv_address)

    dob_sentinel = True
    while(dob_sentinel):
        dob_in = input('Enter date of birth DD/MM/YYYY: ')
        dob_sentinel = False
        if(input_helper.dateVerify(dob_in)):
            pass
        else:
            print("Please us correct format DD/MM/YYYY")
            dob_sentinel=True

    iv_dob_bytes = crypto_helper.gen_16_iv()
    iv_dob = crypto_helper.get_iv_string(iv_dob_bytes)
    dob = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(dob_in,iv_dob)

    phone_number_in = input('Enter your phone number: ')
    iv_phone_number_bytes = crypto_helper.gen_16_iv()
    iv_phone_number = crypto_helper.get_iv_string(iv_phone_number_bytes)
    phone_number = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(phone_number_in,iv_phone_number)

    explicit_consent = input('For the purpose of assessing supports, do you consent to providing personal health information Y\\N: ')
    if(explicit_consent == 'Y' or explicit_consent == 'y'):
        list_disabilities_in = input('Enter your list of disabilities: ')
        iv_list_disabilities_bytes = crypto_helper.gen_16_iv()
        iv_list_disabilities = crypto_helper.get_iv_string(iv_list_disabilities_bytes)
        list_disabilities = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(list_disabilities_in,iv_list_disabilities)
    else:
        list_disabilities_in = 'No explicit consent'
        iv_list_disabilities_bytes = crypto_helper.gen_16_iv()
        iv_list_disabilities = crypto_helper.get_iv_string(iv_list_disabilities_bytes)
        list_disabilities = aes_encrypt_decrypt.encrypt_aes_string_pass_iv(list_disabilities_in,iv_list_disabilities)    

    #print(f"**** Password and Email Reg ****  {email} password {password}")
    #body dictionary replacing password retrieval with keyring

    body = {
        'email': email,
        'email_enc': email_enc,
        'iv_email': iv_email,
        'password': password,
        'salt':salt,
        'displayName': display_name,
        'iv_displayName': iv_displayName,
        'fullname' : fullname,
        'iv_fullname': iv_fullname,
        'address': address,
        'iv_address': iv_address,
        'dob': dob,
        'iv_dob': iv_dob,
        'phone_number': phone_number,
        'iv_phone_number': iv_phone_number,
        'list_disabilities': list_disabilities,
        'iv_list_disabilities': iv_list_disabilities
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

