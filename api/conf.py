import keyring
PORT = 4000
BASE_URL = 'http://localhost:4000/students/'
MONGO_DB_SERVICE = "access_db"
MONGO_DB_USER = "access_db_user"
SERVICE_NAME = 'key_db'
PEPPER = keyring.get_password("pepper_student_app","None")
#Added username and password to authenticated db login
#Use keyring for mongo access, username and password
MONGODB_HOST = {
    'host': 'localhost',
    'port': 27017,
    'username': keyring.get_password(MONGO_DB_USER,"None"),
    'password': keyring.get_password(MONGO_DB_SERVICE,keyring.get_password(MONGO_DB_USER,"None"))
}

MONGODB_DBNAME = 'cyberStudents'

WORKERS = 32

#PARAMS FOR SALT
TEMP_SALT = 'one'
SALT_LENGTH = 32 #Length of derived key
SALT_N = 2**14 #CPU\Memory 16,384
SALT_R = 8 #Block Size
SALT_P = 1 #Parallelism
