from app import mongo
from app.users.services import UserService
import hashlib
from bson.objectid import ObjectId


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

    def get_image(self):
        image = mongo.db[self.base_table].find_one({'is_skipped': False, 'is_labeled': False})
        if not image:
            return False
        return image

    def skip_image(self, _id):
        mongo.db[self.base_table].update({'_id': ObjectId(_id)}, {'$set': {'is_skipped': True}})
        return True

    def rate_image(self, _id, rate):
        try:
            rate = int(rate)
            if rate > 5:
                rate = 5
            mongo.db[self.base_table].update(
                {'_id': ObjectId(_id)},
                {'$set': {'is_labeled': True, 'rate': int(rate)}}
            )
            return True
        except:
            return False
