PORT = 4000
#Added username and password to authenticated db login
#This will use keyring also
MONGODB_HOST = {
    'host': 'localhost',
    'port': 27017,
    'username': "myUserAdmin",
    'password': "admindb"
}

MONGODB_DBNAME = 'cyberStudents'

WORKERS = 32
