
def input_data():
    fullname = input('Please enter your full name: ')
    email = input('Please enter your email')
    address = input('Eneter your full address: ')
    dob = input('Enter your date of birth DD/MM/YYY: ')
    phone_number = input('Enter your phone number: ')
    list_disabilities = input('Enter your list of disabilities: ')
    print(fullname + "\n" + address + "\n" + dob + "\n" + phone_number + "\n" + list_disabilities)

def print_details():
    return None

def register():
    command_curl = 'curl -X POST http://localhost:4000/students/api/login -d '
    command_email = '{\"email\": \"foo@bar.com\",'
    command_password = '\"password\": \"pass\"}"'
    command_token = '{"token": "68fb2bf3b4dd4f48913d27d4e3220140", "expiresIn": 1774798170.719328}'
    full_command = command_curl + command_email + command_password + command_token
    print(full_command)

#Confifure to run as script
if __name__ == '__main__':
    input_data()
    print_details()
    register()