import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

client.testdb.add_user('faruk', '1234', roles=[{'role':'readWrite','db':'vrdata'}])