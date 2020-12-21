from app import mongo
from app.users.services import UserService
import hashlib


class RatingService:
    def __init__(self):
        u = UserService()
        self.user = u.user
        self.role = u.role

        self.base_table = '{}_{}'.format(
            self.user['username'], hashlib.md5(self.user['username'].encode('utf-8')).hexdigest()
        )

    def get_total(self, q={}):
        if not q:
            return mongo.db[self.base_table].find().count()
        return mongo.db[self.base_table].find(q).count()
