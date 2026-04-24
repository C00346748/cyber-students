import asyncio
import crypto_helper
import aes_encrypt_decrypt
import pwinput
import click

from tornado.httpclient import AsyncHTTPClient
from json import dumps
from tornado.escape import json_decode
from api.conf import SERVICE_NAME, MONGODB_DBNAME, WORKERS, MONGODB_HOST, BASE_URL
from motor.motor_tornado import MotorClient

async def cli_login():
    email = aes_encrypt_decrypt.encrypt_aes_string(input('Please enter your email: '))
    #email_in = input('Please enter your email: ')
    password = pwinput.pwinput('Enter your password: ')
    
    #get the salt from the database and combine with password
    db = MotorClient(**MONGODB_HOST)[MONGODB_DBNAME]
    print(email)
    cur = db.users.find({}, {
        'email': 1,
        'password': 1,
        'salt': 1,
        'displayName': 1,
        'fullname': 1,
        'address': 1,
        'dob': 1,
        'phone_number': 1,
        'list_disabilities': 1,
        'token': 1,
        'expiresIn': 1,
    })
    docs = await cur.to_list(length=None)
    for doc in docs:
        click.echo(doc)
    
    print("Next")

    user_salt = await db.users.find_one({
        'email': email
    }, {
        'salt': 1
    })
    salt = user_salt['salt']
    print(salt)

    user_password = await db.users.find_one({
        'email': email
    }, {
        'password': 1
    })
    password_out = user_password['password']
    print(password_out)

    unsalt_pwd = crypto_helper.un_salt(crypto_helper.add_pepper(password),salt)
    print(unsalt_pwd[0])
    if(password==password):
        print("Password match")

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
    asyncio.run(cli_login())