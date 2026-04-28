import logging
import unittest

from test.login import LoginHandlerTest
from test.logout import LogoutHandlerTest
from test.registration import RegistrationHandlerTest
from test.user import UserHandlerTest
from test.welcome import WelcomeHandlerTest
from test.crypto import CryptoTest

#Configure to run as script
if __name__ == '__main__':
    #Logging is disabled
    logging.getLogger('tornado.access').disabled = True
    unittest.main()
