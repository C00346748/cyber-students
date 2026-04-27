from tornado.httpclient import AsyncHTTPClient
from json import dumps
from tornado.escape import json_decode
from api.conf import SERVICE_NAME, MONGODB_DBNAME, WORKERS, MONGODB_HOST, BASE_URL
from motor.motor_tornado import MotorClient

import click
import asyncio
import crypto_helper
import aes_encrypt_decrypt
import tracemalloc
import cli_login_user

db = MotorClient(**MONGODB_HOST)[MONGODB_DBNAME]

#Retrieve all data for the user email from DB
async def view_my_data():    
    tracemalloc.start()
    email=crypto_helper.simple_hash('luke@luke.com')
    print("Data registered under your account: ")

    user_data = await db.users.find_one(
        {'email': email},
        {'email_enc': 1,'iv_email': 1,'displayName': 1,'iv_displayName': 1,'fullname': 1,'iv_fullname': 1,'address': 1,'iv_address': 1,'dob': 1,'iv_dob': 1,'phone_number': 1,'iv_phone_number': 1, 'list_disabilities': 1, 'iv_list_disabilities': 1}
    )

    #Get and display email
    email_str = str(user_data['email_enc'])
    email_iv_str = str(user_data['iv_email'])
    dec_email = aes_encrypt_decrypt.decrypt_aes_string_pass_iv(email_str,email_iv_str)
    print("E-mail:\t\t\t" + dec_email)

    #Get and full name
    displayName_str = str(user_data['displayName'])
    displayName_iv_str = str(user_data['iv_displayName'])
    dec_displayName = aes_encrypt_decrypt.decrypt_aes_string_pass_iv(displayName_str,displayName_iv_str)
    print("Display Name:\t\t" + dec_displayName)

    #Get and full name
    fullname_str = str(user_data['fullname'])
    fullname_iv_str = str(user_data['iv_fullname'])
    dec_fullname = aes_encrypt_decrypt.decrypt_aes_string_pass_iv(fullname_str,fullname_iv_str)
    print("Fullname:\t\t" + dec_fullname)

    #Get and decrypt address
    address_str = str(user_data['address'])
    address_iv_str = str(user_data['iv_address'])
    dec_address = aes_encrypt_decrypt.decrypt_aes_string_pass_iv(address_str,address_iv_str)
    print("Address:\t\t" + dec_address)

    #Get and decrypt dob
    dob_str = str(user_data['dob'])
    dob_iv_str = str(user_data['iv_dob'])
    dec_dob = aes_encrypt_decrypt.decrypt_aes_string_pass_iv(dob_str,dob_iv_str)
    print("Date-of-birth:\t\t" + dec_dob)


    #Get and decrypt list_disabilities
    list_disabilities_str = str(user_data['list_disabilities'])
    list_disabilities_iv_str = str(user_data['iv_list_disabilities'])
    dec_list_disabilities = aes_encrypt_decrypt.decrypt_aes_string_pass_iv(list_disabilities_str,list_disabilities_iv_str)
    print("List of disabilities:\t" + dec_list_disabilities)

    #Get and decrypt phone_number
    phone_number_str = str(user_data['phone_number'])
    phone_number_iv_str = str(user_data['iv_phone_number'])
    dec_phone_number = aes_encrypt_decrypt.decrypt_aes_string_pass_iv(phone_number_str,phone_number_iv_str)
    print("Phone Number:\t\t" + dec_phone_number)

async def welcome():
    http_client = AsyncHTTPClient()
    url = BASE_URL + "api/"
    
    response = await http_client.fetch(
        url,
        method="GET"
    )

    body = json_decode(response.body)
    print(body['message'])

#Configure to run as script
if __name__ == '__main__':
    asyncio.run(welcome())
    #No login success no view of data
    if(asyncio.run(cli_login_user.cli_login())):
        asyncio.run(view_my_data())