from app import mongo, login, bcrypt


# login manager
class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        return bcrypt.check_password_hash(password_hash, password)

    @login.user_loader
    def load_user(username):
        u = mongo.db.users.find_one({'username': username})
        if not u:
            return None
        return User(username=u['username'])
