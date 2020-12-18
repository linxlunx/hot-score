from app import mongo, bcrypt
from getpass import getpass
from app.util.regex import valid_username, valid_email
import sys
import hashlib


def create_superuser():
    print('=' * 20)
    print('This command will create superuser')
    print('=' * 20)

    if mongo.db.base_images.count() == 0:
        print('Please import base image first!')
        sys.exit()

    while True:
        while True:
            username = input('Username: ')
            if not username:
                print('Username cannot be blank!')
                continue

            if not valid_username(username):
                print('Username is not valid, only allow alphanumeric and underscore character!')
                continue
            break

        while True:
            email = input('Email: ')
            if not email:
                print('Email cannot be blank!')
                continue

            if not valid_email(email):
                print('Email format is not valid!')
                continue
            break

        while True:
            password = getpass('Password: ')
            if not password:
                print('Password cannot be blank!')
                continue

            password_confirmation = getpass('Confirm Password: ')
            if not password_confirmation:
                print('Confirmation password cannot be blank!')
                continue

            if password != password_confirmation:
                print('Password and confirmation must be same!')
                continue

            break

        check_username_email = mongo.db.users.find_one({
            '$or': [
                {'username': username},
                {'email': email}
            ]
        })

        if check_username_email:
            print('Another username/email has been registered. Please choose another one!')
            continue

        break

    # insert user
    user = mongo.db.users.insert({
        'username': username,
        'email': email,
        'password': bcrypt.generate_password_hash(password).decode('utf-8'),
        'role': 'admin',
        'active': True
    })

    # copy collection
    user_table = '{}_{}'.format(username, hashlib.md5(username.encode('utf-8')).hexdigest())
    pipeline = [
        {'$match': {}},
        {'$out': user_table},
    ]
    mongo.db.base_images.aggregate(pipeline)
    mongo.db[user_table].create_index('is_skipped', background=True)
    mongo.db[user_table].create_index('is_labeled', background=True)

    print('Successfully created user {}'.format(username))
