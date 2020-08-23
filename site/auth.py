import jwt

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
            self.vrdata = client["vrdata"]

        else:
            print('VRdata is not available.')
            self.vrdata = None

    def verify(self,user,password):

        selected = self.vrdata['users'].find_one({'user':user})

        if selected is None:
            return None

        return selected['password'] == password

    def token(self,user,password):
        from datetime import datetime, timedelta

        JWT_SECRET = 'secret'
        JWT_ALGORITHM = 'HS256'
        JWT_EXP_DELTA_SECONDS = 20

        selected = self.vrdata['users'].find_one({'user':user})

        payload = {
            'user_id': str(selected['_id']),
            'exp': str(datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS))
        }
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        return jwt_token.decode('utf-8')


    


        