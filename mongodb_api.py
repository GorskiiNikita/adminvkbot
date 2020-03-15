from pymongo import MongoClient
from datetime import datetime


class MongoApi:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.botdb

    def get_list_of_groups(self):
        groups = []
        for group in self.db.groups.find():
            groups.append(group['_id'])
        return groups

    def get_users(self):
        users = []
        for user in self.db.users.find():
            users.append(user['_id'])
        return users

    def add_group(self, group):
        self.db.groups.insert_one(group)

    def delete_group(self, group_id):
        self.db.groups.remove({'_id': group_id})

    def get_group(self, group_id):
        return self.db.groups.find_one({'_id': group_id})

    def update_group(self, group_id, data):
        self.db.groups.update_one({
            '_id': group_id
        }, {
            '$set': data
        }, upsert=False)

    def get_texts(self):
        texts = []
        for text in self.db.texts.find():
            texts.append(text)
        return texts

    def update_texts(self, texts):
        for key in texts.keys():
            self.db.texts.update_one({
                '_id': key
            }, {
                '$set': {'text': texts[key]}
            }, upsert=False)

    def update_time_texts(self):
        now = int(datetime.now().timestamp())
        self.db.times.update_one({
            '_id': 'last_update_texts'
        }, {
            '$set': {'timestamp': now}
        }, upsert=False)

    def update_time_groups(self):
        now = int(datetime.now().timestamp())
        self.db.times.update_one({
            '_id': 'last_update_groups'
        }, {
            '$set': {'timestamp': now}
        }, upsert=False)


mongo_client = MongoApi()
