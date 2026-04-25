import asyncio
import crypto_helper
import aes_encrypt_decrypt
import pwinput
import click

from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import HTTPHeaders
from json import dumps
from tornado.escape import json_decode
from api.conf import SERVICE_NAME, MONGODB_DBNAME, WORKERS, MONGODB_HOST, BASE_URL
from motor.motor_tornado import MotorClient

async def cli_logout():
    email = crypto_helper.simple_hash(input('Please enter your email: '))
    http_client = AsyncHTTPClient()
    url = BASE_URL + "api/logout"

    db = MotorClient(**MONGODB_HOST)[MONGODB_DBNAME]

    user_token = await db.users.find_one({
        'email': email
    }, {
        'token': 1
    })
    token = user_token['token']

    print("Token " + token)

    headers = HTTPHeaders({'X-Token': token})
    body = {}

    response = await http_client.fetch(
        url,
        method="POST",
        body=dumps(body),
        headers=headers
    )

    body = json_decode(response.body)
    print(body['message'])


#Configure to run as script
if __name__ == '__main__':
    asyncio.run(cli_logout())