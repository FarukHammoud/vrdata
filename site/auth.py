class User:

    def __init__(self,id,name,password):
        self.id = id
        self.name = name
        self.password = password

class Auth:

    def __init__(self):
        # Check MongoDB Server access
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        if 'vrdata' in client.list_database_names():
            print('VRdata is available.')
            vrdata = client["vrdata"]
        else:
            print('VRdata is not available.')
            vrdata = None
    


        