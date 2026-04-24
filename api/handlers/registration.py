from tornado.escape import json_decode

from .base import BaseHandler

class RegistrationHandler(BaseHandler):

    async def post(self):
        try:
            body = json_decode(self.request.body)
            #Removed the strip and smalls because it doesn't work with encypted text
            email = body['email']
            password = body['password']
            salt = body['salt']
            display_name = body.get('displayName')
            fullname = body.get('fullname')
            address = body.get('address')
            dob = body.get('dob')
            phone_number = body.get('phone_number')
            list_disabilities = body.get('list_disabilities')
            if display_name is None:
                display_name = email
            if not isinstance(display_name, str):
                raise Exception('Display name must be a string')
        except Exception:
            self.send_error(400, message='You must provide an email address, password and display name!')
            return

        if not email:
            self.send_error(400, message='The email address is invalid!')
            return

        if not password:
            self.send_error(400, message='The password is invalid!')
            return
        
        if not salt:
            self.send_error(400, message='Salt error!')
            return

        if not display_name:
            self.send_error(400, message='The display name is invalid!')
            return
        
        if not fullname:
            self.send_error(400, message='The full name is invalid!')
            return        

        if not address:
            self.send_error(400, message='The address is invalid!')
            return          
        
        if not dob:
            self.send_error(400, message='The dob is invalid!')
            return 
        
        if not phone_number:
            self.send_error(400, message='The phone number is invalid!')
            return
        
        if not list_disabilities:
            self.send_error(400, message='The disability list had errors!')
            return       
         
        user = await self.db.users.find_one({
          'email': email
        })

        if user is not None:
            self.send_error(409, message='A user with the given email address already exists!')
            return

        await self.db.users.insert_one({
            'email': email,
            'password': password,
            'salt': salt,
            'displayName': display_name,
            'fullname': fullname,
            'address': address,
            'dob': dob,
            'phone_number': phone_number,
            'list_disabilities': list_disabilities
        })

        self.set_status(200)
        self.response['email'] = email
        self.response['displayName'] = display_name

        self.write_json()