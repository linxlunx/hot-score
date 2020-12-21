from app import mongo
from flask_login import current_user
import hashlib


class UserService():
    def __init__(self):
        self.user = mongo.db.users.find_one({'username': current_user.username})
        self.role = self.user['role']

    def user_get(self, username):
        if current_user.username != username:
            if self.role != 'admin':
                return False
        user = mongo.db.users.find_one({'username': username})
        if not user:
            return False
        return user

    def user_list(self):
        users = []
        if self.role == 'admin':
            users_q = mongo.db.users.find()
        else:
            users_q = mongo.db.users.find({'username': current_user.username})
        for u in users_q:
            users.append({
                'username': u['username'],
                'email': u['email'],
                'role': u['role'],
                'status': 'Active' if u['active'] else 'Inactive'
            })
        return users

    def user_update(self, username, data):
        if self.role != 'admin':
            username = self.user['username']

        mongo.db.users.update_one({
            'username': username
        }, {
            '$set': data
        })
        return True

    def user_store(self, data):
        if self.role != 'admin':
            return False
        # insert user
        mongo.db.users.insert(data)

        # copy collection data
        user_table = '{}_{}'.format(data['username'], hashlib.md5(data['username'].encode('utf-8')).hexdigest())
        pipeline = [
            {'$match': {}},
            {'$out': user_table},
        ]
        mongo.db.base_images.aggregate(pipeline)
        mongo.db[user_table].create_index('is_skipped', background=True)
        mongo.db[user_table].create_index('is_labeled', background=True)
        return True

    def email_is_exist(self, email):
        email_exist = mongo.db.users.find_one({'active': True, 'email': email})
        if not email_exist:
            return False
        return email_exist

    def check_email_change(self, email, user):
        email_exist = self.email_is_exist(email)
        if not email_exist:
            return False

        if email_exist:
            if email_exist['username'] != user['username']:
                return True
            else:
                return False


