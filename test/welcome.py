from tornado.escape import json_decode
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from api.handlers.welcome import WelcomeHandler

from .base import BaseTest

#Loads Welcome page of webserver
class WelcomeHandlerTest(BaseTest):

    #Application loads 
    @classmethod
    def setUpClass(self):
        self.my_app = Application([(r'/welcome', WelcomeHandler)])
        super().setUpClass()

    #Test it loads welcome page on webserver
    def test_welcome(self):
        response = self.fetch('/welcome')
        self.assertEqual(200, response.code)

        body = json_decode(response.body)
        self.assertIsNotNone(body['message'])
