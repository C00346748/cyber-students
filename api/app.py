from concurrent.futures import ThreadPoolExecutor
from motor.motor_tornado import MotorClient
from tornado.web import Application

from .conf import MONGODB_HOST, MONGODB_DBNAME, WORKERS

from .handlers.welcome import WelcomeHandler
from .handlers.registration import RegistrationHandler
from .handlers.login import LoginHandler
from .handlers.logout import LogoutHandler
from .handlers.user import UserHandler

class Application(Application):

    #Starts the App
    def __init__(self):
        handlers = [
            (r'/students/?', WelcomeHandler),
            (r'/students/api/?', WelcomeHandler),
            (r'/students/api/registration', RegistrationHandler),
            (r'/students/api/login', LoginHandler),
            (r'/students/api/logout', LogoutHandler),
            (r'/students/api/user', UserHandler)
        ]

        settings = dict()

        super(Application, self).__init__(handlers, **settings)

        #Looks like its connecting and sending the host and db name to connect
        # MONGODB_HOST is unpacked dictionary with 'host' = 'localhost' and 'port': 27017
        # and MONGODB_NAME 'cyberStudents'
        # This info is read from conf.py
        # Motor client is imported from motor.motor_tornado
        self.db = MotorClient(**MONGODB_HOST)[MONGODB_DBNAME]

        #Possible addition of authenticated db connection
        #self.db = MotorClient("mongodb://admin:password@ds047057.mongolab.com:47057/[MONGODB_DBNAME]").open_sync().[MONGODB_DBNAME]

        self.executor = ThreadPoolExecutor(WORKERS)
