from json import dumps
from tornado.escape import json_decode
from tornado.httputil import HTTPHeaders
from tornado.ioloop import IOLoop
from tornado.web import Application
from test.conf import SERVICE_NAME, PRV_KEY, PUB_KEY
from cryptography.hazmat.primitives import hashes, serialization
from motor.motor_tornado import MotorClient

import asyncio
import keyring
import aes_encrypt_decrypt

from api.handlers.user import UserHandler
from api.handlers.registration import RegistrationHandler
from concurrent.futures import ThreadPoolExecutor
from mongomock_motor import AsyncMongoMockClient
from test.base import BaseTest

from test.conf import MONGODB_DBNAME, WORKERS, MONGODB_HOST

db = None

async def register():
    my_app = Application([(r'/registration', RegistrationHandler)])
    my_app.db = AsyncMongoMockClient()[MONGODB_DBNAME]
    my_app.executor = ThreadPoolExecutor(WORKERS)
    db = MotorClient(**MONGODB_HOST)[MONGODB_DBNAME]
    await my_app.db.users.insert_one({
        'email': 'luke@luke.com',
        'password': 'password',
        'displayName': 'testDisplayName'
    })



#Confifure to run as script
if __name__ == '__main__':
    register()
