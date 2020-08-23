import pymongo

client = pymongo.MongoClient("mongodb://vrdata.viarezo.fr:27017/")

vrdata = client["vrdata"]

collection = vrdata["customers"]

mydict = { "name": "John", "address": "Highway 37" }

x = collection.insert_one(mydict)

dbs = client.list_database_names()

print(dbs)
