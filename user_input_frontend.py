import crypto_helper
from tornado.web import Application
from api.handlers.registration import RegistrationHandler
import subprocess

def input_data():
    fullname = input('Please enter your full name: ')
    email = input('Please enter your email')
    address = input('Eneter your full address: ')
    dob = input('Enter your date of birth DD/MM/YYY: ')
    phone_number = input('Enter your phone number: ')
    list_disabilities = input('Enter your list of disabilities: ')
    print(fullname + "\n" + address + "\n" + dob + "\n" + phone_number + "\n" + list_disabilities)
    register_full(fullname,email,address,dob,phone_number,list_disabilities)

def limited_data():
    email = input('Please enter your email')
    password = input('Enter your password: ')
    displayName = input('Enter the display name to use')

    reg_basic_enc(email,password,displayName)

def print_details():
    return None

async def reg_exe(email,password,displayName):
    my_app = Application([(r'/registration', RegistrationHandler)])
    await my_app.db.users.insert_one({
        'email': email,
        'password': password,
        'displayName': displayName
    })

def reg():
    my_app = Application([(r'/registration', RegistrationHandler)])
    email = crypto_helper.encrypt_email('test@test.com')
    displayName = crypto_helper.encrypt_other_string('test@test.com','testDisplayName')
    #print(f"Salt and peppered display name {display_name}")
    password = crypto_helper.encrypt_pwd('test@test.com')
    #print(f"**** Password and Email Reg ****  {email} password {password}")
    #body dictionary replacing password retrieval with keyring
    body = {
        'email': email,
        'password': password,
        'displayName': displayName
    }
    reg(email,password,displayName)
    print("Reg of test@test.com")

def reg_basic(email,password,displayName):
    command = fr'curl -X POST http://localhost:4000/students/api/registration -d "{{\"email\": \"{email}\", \"password\": \"{password}\", \"displayName\": \"{displayName}\"}}"'
    try:
        run = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print("Run: ", run.stdout)
    except subprocess.CalledProcessError as error:
        print("Run error: ", error.stderr)    


def reg_basic_enc(email,password,displayName):
    command = fr'curl -X POST http://localhost:4000/students/api/registration -d "{{\"email\": \"{crypto_helper.encrypt_email(email)}\", \"password\": \"{crypto_helper.encrypt_pwd(password)}\", \"displayName\": \"{crypto_helper.encrypt_other_string(email,displayName)}\"}}"'
    try:
        run = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print("Run: ", run.stdout)
    except subprocess.CalledProcessError as error:
        print("Run error: ", error.stderr) 


def register_full(fullname,email,address,dob,phone_number,list_disabilities):
    command = fr'curl -X POST http://localhost:4000/students/api/registration -d "{{\"email\": \"{email}\", \"fullname\": \"{fullname}\", \"address\": \"{address}\", \"dob\": \"{dob}\", \"phone_number\": \"{phone_number}\", \"list_disabilities\": \"{list_disabilities}\"}}"'
    try:
        run = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print("Run: ", run.stdout)
    except subprocess.CalledProcessError as error:
        print("Run error: ", error.stderr) 

def sec_register(fullname,email,address,dob,phone_number,list_disabilities):
    db_user = "admin"
    db_pass = "secure_password"
    command = fr'curl -u "{db_user}:{db_pass}" -X POST http://localhost:4000/students/api/registration -d "{{\"email\": \"{email}\", \"fullname\": \"{fullname}\", \"address\": \"{address}\", \"dob\": \"{dob}\", \"phone_number\": \"{phone_number}\", \"list_disabilities\": \"{list_disabilities}\"}}"'

#curl -X POST http://localhost:4000/students/api/registration -d "{\"email\": \"foo@bar.com\", \"password\": \"pass\", \"displayName\": \"Foo Bar\"}"
#Confifure to run as script
if __name__ == '__main__':
    limited_data()
    #reg()