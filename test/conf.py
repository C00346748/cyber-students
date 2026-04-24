import keyring

#Add service name
SERVICE_NAME = 'key_db'
PUB_KEY = keyring.get_password("hash_pub","None")
PRV_KEY = keyring.get_password("hash_prv","None")

#PARAMS FOR SALT
SALT_LENGTH = 64 #Length of derived key
SALT_N = 2**14 #CPU\Memory 16,384
SALT_R = 8 #Block Size
SALT_P = 1 #Parallelism

PEPPER = keyring.get_password("pepper_student_app","None")

PORT = 4000
MONGO_DB_SERVICE = "access_db"
MONGO_DB_USER = "access_db_user"
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
