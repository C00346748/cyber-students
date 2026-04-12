import asyncio
import click
import aes_encrypt_decrypt
from json import loads
from motor.motor_tornado import MotorClient

#The configure file has the login details
from api.conf import MONGODB_HOST, MONGODB_DBNAME

#enc = aes_encrypt_decrypt.encrypt("This is the text to decrypt")
#print(enc)
#dec = aes_encrypt_decrypt.decrypt(enc)
#print(dec)

#Queries mongo for info
async def get_users(db):
  cur = db.users.find({}, {
    'email': 1,
    'password': 1,
    'displayName': 1,
    'fullname': 1,
    'address': 1,
    'dob': 1,
    'token': 1,
    'expiresIn': 1,
  })
  docs = await cur.to_list(length=None)
  print('There are ' + str(len(docs)) + ' registered users:')
  for doc in docs:
    click.echo(doc)

#This is just passing when tested, not really implementing anything
@click.group()
def cli():
    pass

@cli.command()
def list():
    #Connecting to the database using the HOST Details and Name
    #The DB now requires authentication but it has access to .conf
    db = MotorClient(**MONGODB_HOST)[MONGODB_DBNAME]
    asyncio.run(get_users(db))

#Confifure to run as script
if __name__ == '__main__':
    cli()
