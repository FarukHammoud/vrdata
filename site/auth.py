import jwt

class User:

    def __init__(self,id,name,password):
        self.id = id
        self.name = name
        self.password = password

class Auth:

    def __init__(self):

        self.admin_username = None
        self.admin_password = None

        self.import_credentials()
        self.login()

    def import_credentials(self):
        import os.path
        # Check if credentials file exists and upload admin credentials
        if os.path.isfile('credentials'):
            f = open("credentials", 'r')
            lines = f.readlines()  # array of file lines
            self.admin_username = lines[0]
            self.admin_password = lines[1]
            f.close()

        # Otherwise ask for credentials and save it in the file
        else:
            self.admin_username = input('username: ')
            self.admin_password = input('password: ')
            y_n = input('Do you want to save them? (y or n)')

            if y_n == 'y':
                with open('credentials', 'a') as f: # able to append data to file
                    f.write(self.admin_username) # Were var1 is some variable you have set previously
                    f.write(self.admin_password) 
                    f.close() # You can add this but it is not mandatory 
    
    def login(self):
         # Check MongoDB Server access

        import pymongo
        self.client = pymongo.MongoClient("mongodb://localhost:27017/",username=self.admin_username,password=self.admin_password,authSource='admin')

        if 'vrdata' in self.client.list_database_names():
            print('VRdata is available.')
            self.vrdata = self.client["vrdata"]

        else:
            print('VRdata is not available.')
            self.vrdata = None

    def VRify(self,username,password):
        import requests

        url = 'https://test.auth.viarezo.fr/oauth/token'
        myobj = {'grant_type':'password','client_id':'b21c69c5569bda11a0005cf2515b74471eb33c99','client_secret':'95322a9340e0eddf70316b402e1a47917ed89669','scope':'default','username':username,'password':password}

        r = requests.post(url, data = myobj)

        if 'access_token' in r.json():
            self.vr_token = r.json()['access_token']
            print(self.vr_token)
            return True
        else:
            self.token = None
            return False

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


    


        