import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

vrdata = client["vrdata"]

collection = vrdata["users"]

mydict = { "user": "2019hammoudf", "password": "abcd1234" }

x = collection.insert_one(mydict)

dbs = client.list_database_names()

print(dbs)

selected = vrdata['users'].find_one({'user':'2019hammoudf'})

print(selected['password'])