 # Check MongoDB Server access

import pymongo

client = pymongo.MongoClient('vrdata.viarezo.fr',username='faruk',password='1234',authSource='vrdata')

if 'vrdata' in client.list_database_names():
    print('VRdata is available.')
    vrdata = client["vrdata"]
    selected = vrdata['users'].find_one({'user':'2019hammoudf'})

print(selected['password'])

else:
    print('VRdata is not available.')
    vrdata = None