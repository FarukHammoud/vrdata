import pymongo

client = pymongo.MongoClient('vrdata.viarezo.fr',username='root',password='root',authSource='admin')

client['db1'].add_user('2019hammoudf', 'eyJ0eXAiOiJKV1Qi', roles=[{'role':'readWrite','db':'db1'}])

