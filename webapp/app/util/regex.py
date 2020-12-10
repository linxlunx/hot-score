import re


def valid_username(word):
    if re.match(r'^[a-zA-Z0-9_]+$', word):
        return True
    return False


def valid_email(email):
    mail_match = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'
    if re.match(mail_match, email):
        return True
    return False
