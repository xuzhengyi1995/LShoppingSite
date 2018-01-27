# For Database use
# XUZhengyi, 22/01/2018

import pymongo
try:
    from common import settings
except:
    import settings
import pprint


class Db:
    '''
    For mongodb
    '''

    def __init__(self, ssl=False):
        self.ip = settings.mongodb_ip
        self.db = settings.mongodb_db
        self.ssl = ssl
        self.client = pymongo.MongoClient(self.ip, ssl=self.ssl)

    def getDB(self, dbname=False):
        _database = self.client[self.db] if(not dbname) else _client[dbname]
        return _database

    def getCollection(self, collection):
        _db = self.getDB()
        if(not collection in _db.collection_names(include_system_collections=False)):
            raise(Exception('Do not have collection \'%s\'.' % collection))
        co = _db[collection]
        return co


if __name__ == '__main__':
    testdb = Db()
    #testdb.getCollection('products').update_one({'id': 80461}, {'$set': {'price': 16.99}})
    #r = testdb.getCollection('products').find_one({'id': 80461}, projection={'price': True})
    r = testdb.getCollection('products')

    print(r)
    # testdb.getCollection('pro')
