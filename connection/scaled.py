import pymongo

myclient = pymongo.MongoClient("mongodb://vrdata.viarezo.fr:27017/")

mydb = myclient["mydatabase"]
print(myclient.list_database_names())