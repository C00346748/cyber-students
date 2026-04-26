from email_validator import validate_email, EmailNotValidError

MIN_PASSWORD_LENGTH = 6

def verifyEmail(email):
    try:
        # Check syntax and if the domain has a valid MX record
        valid = validate_email(email)
        
        # Use the normalized form (e.g., lowercase)
        normalized_email = valid.email
    except EmailNotValidError as e:
        print(f"Invalid Email format: {str(e)}")
        return False
    return True

def verifyPasswordLengthOnly(password):
    if(len(password)>MIN_PASSWORD_LENGTH):
        caps = any(char.isupper() for char in password)
        number = any(char.isdigit() for char in password)
        if caps and number:
            return True
    else:
        return False