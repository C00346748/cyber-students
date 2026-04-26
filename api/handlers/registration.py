from tornado.escape import json_decode

from .base import BaseHandler

class RegistrationHandler(BaseHandler):

    async def post(self):
        try:
            body = json_decode(self.request.body)
            #Removed the strip and smalls because it doesn't work with encypted text
            email = body['email']
            email_enc = body['email_enc']
            iv_email = body['iv_email']
            password = body['password']
            salt = body['salt']
            display_name = body.get('displayName')
            iv_displayName = body.get('iv_displayName')
            fullname = body.get('fullname')
            iv_fullname = body.get('iv_fullname')
            address = body.get('address')
            iv_address = body.get('iv_address')
            dob = body.get('dob')
            iv_dob = body.get('iv_dob')
            phone_number = body.get('phone_number')
            iv_phone_number = body.get('iv_phone_number')
            list_disabilities = body.get('list_disabilities')
            iv_list_disabilities = body.get('iv_list_disabilities')
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
        
        if not email_enc:
            self.send_error(400, message='The email address is invalid!')
            return

        if not iv_email:
            self.send_error(400, message='The email address is invalid!')
            return

        #DisplayName not required
        #if not iv_displayName:
            #self.send_error(400, message='The email address is invalid!')
            #return

        if not password:
            self.send_error(400, message='The password is invalid!')
            return
        
        if not salt:
            self.send_error(400, message='Salt error!')
            return

        #DisplayName not required
        #if not display_name:
            #self.send_error(400, message='The display name is invalid!')
            #return
        
        if not fullname:
            self.send_error(400, message='The full name is invalid!')
            return  

        if not iv_fullname:
            self.send_error(400, message='The full name is invalid!')
            return  

        if not address:
            self.send_error(400, message='The address is invalid!')
            return          
        
        if not iv_address:
            self.send_error(400, message='The address is invalid!')
            return          

        if not dob:
            self.send_error(400, message='The dob is invalid!')
            return 
        
        if not iv_dob:
            self.send_error(400, message='The dob is invalid!')
            return 

        if not phone_number:
            self.send_error(400, message='The phone number is invalid!')
            return
        
        if not iv_phone_number:
            self.send_error(400, message='The phone number is invalid!')
            return

        if not list_disabilities:
            self.send_error(400, message='The disability list had errors!')
            return       

        if not iv_list_disabilities:
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
            'email_enc': email_enc,
            'iv_email': iv_email,
            'password': password,
            'salt': salt,
            'displayName': display_name,
            'iv_displayName': iv_displayName,
            'fullname': fullname,
            'iv_fullname': iv_fullname,
            'address': address,
            'iv_address': iv_address,
            'dob': dob,
            'iv_dob': iv_dob,
            'phone_number': phone_number,
            'iv_phone_number': iv_phone_number,
            'list_disabilities': list_disabilities,
            'iv_list_disabilities': iv_list_disabilities
        })

        self.set_status(200)
        self.response['email'] = email
        self.response['displayName'] = display_name

        self.write_json()