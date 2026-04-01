import keyring
PORT = 4000
MONGO_DB_SERVICE = "access_db"
#Added username and password to authenticated db login
#Use keyring for mongo access
MONGODB_HOST = {
    'host': 'localhost',
    'port': 27017,
    'username': "myUserAdmin",
    'password': keyring.get_password(MONGO_DB_SERVICE,"myUserAdmin")
}

MONGODB_DBNAME = 'cyberStudents'

WORKERS = 32
