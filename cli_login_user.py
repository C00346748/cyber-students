import asyncio
import crypto_helper
import aes_encrypt_decrypt
import pwinput
import click
from uuid import uuid4

from tornado.httpclient import AsyncHTTPClient
from json import dumps
from tornado.escape import json_decode
from api.conf import SERVICE_NAME, MONGODB_DBNAME, WORKERS, MONGODB_HOST, BASE_URL
from motor.motor_tornado import MotorClient

async def cli_login():
    email = crypto_helper.simple_hash(input('Please enter your email: '))
    print("Email: " + email)
    #email_in = input('Please enter your email: ')
    salt = None
    #get the salt from the database and combine with password
    db = MotorClient(**MONGODB_HOST)[MONGODB_DBNAME]

    #Get salt and iv from the DB to season the password entered
    try:
        user_salt = await db.users.find_one({
            'email': email
        }, {
            'salt': 1
        })
        salt = user_salt['salt']
    except:
        pass #Don't want to give a clue that username is wrong
    try: #Separate try to avoid all the server error messages showing giving error details
        unsalt_pwd = crypto_helper.season(crypto_helper.add_pepper(pwinput.pwinput('Enter your password: ')),salt)

        body = {
            'email': email,
            'password': unsalt_pwd
        }

        http_client = AsyncHTTPClient()
        url = BASE_URL + "api/login"
        #Send request to registration handler
        #response = my_app.start_request('/registration', method='POST', body=dumps(body))
        
        response = await http_client.fetch(
            url,
            method="POST",
            body=dumps(body),
            headers={"Content-Type": "application/json"}
        )
        print(f"Server response {response.code}")
        body = json_decode(response.body)
        print(body['message'])
    except:
        print("Error with login")

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
    asyncio.run(cli_login())