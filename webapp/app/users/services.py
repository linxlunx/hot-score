from app import mongo
from flask_login import current_user


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

    def check_email(self, email, user):
        email_exist = mongo.db.users.find_one({'active': True, 'email': email})
        if not email_exist:
            return False

        if email_exist:
            if email_exist['username'] != user['username']:
                return True
            else:
                return False
