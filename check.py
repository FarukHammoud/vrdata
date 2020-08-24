 # Check MongoDB Server access

import pymongo
client = pymongo.MongoClient("mongodb://vrdata.viarezo.fr")

if 'vrdata' in client.list_database_names():
    print('VRdata is available.')
    vrdata = client["vrdata"]

else:
    print('VRdata is not available.')
    vrdata = None