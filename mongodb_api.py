from pymongo import MongoClient


class MongoApi:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.botdb

    def get_list_of_groups(self):
        groups = []
        for group in self.db.groups.find():
            groups.append(group['_id'])
        return groups

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


mongo_client = MongoApi()
