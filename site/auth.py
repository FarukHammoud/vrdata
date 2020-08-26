import jwt

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
            self.admin_username = lines[0].strip('\n')
            self.admin_password = lines[1].strip('\n')
            f.close()

        # Otherwise ask for credentials and save it in the file
        else:
            print('Enter your VRdata admin credentials ->')
            self.admin_username = input('username: ')
            self.admin_password = input('password: ')
            y_n = input('Do you want to save them? (y or n) ')

            if y_n == 'y':
                f = open('credentials', 'w') 
                f.write(self.admin_username+'\n'+self.admin_password+'\n')
                f.close() # You can add this but it is not mandatory 
    
    def login(self):
         # Check MongoDB Server access

        import pymongo
        self.client = pymongo.MongoClient("mongodb://localhost:27017/",username=self.admin_username,password=self.admin_password,authSource='admin')

        if 'vrdata' in self.client.list_database_names():
            print('VRdata is online.')
            self.vrdata = self.client["vrdata"]

        else:
            print('VRdata is not available.')
            self.vrdata = None

    def VRify(self,username,password):
        import requests

        url = 'https://test.auth.viarezo.fr/oauth/token'
        myobj = {'grant_type':'password','client_id':'b21c69c5569bda11a0005cf2515b74471eb33c99','client_secret':'95322a9340e0eddf70316b402e1a47917ed89669','scope':'default','username':username,'password':password}

        ans = requests.post(url, data = myobj)

        if 'access_token' in ans.json():
            vr_token = ans.json()['access_token']
            return vr_token
        else:
            return None

    def user_exists(self,user,db_name):

        if db_name in self.client.list_database_names():
            print('VRdata is online.')
        selected = self.vrdata['users'].find_one({'user':user,'db_name':db_name})
        return not (selected is None)

    def create_user(self,user,token,db_name):
        print('Creating user',user,token,db_name)
        new_user = { "user": user, 'db_name':db_name}
        self.vrdata['users'].insert_one(new_user)
    
    def refresh_token(self,user,jwt_token,db_name):
        complete_token = jwt_token.decode('utf-8')
        token = complete_token[0:16]

        tokens = self.vrdata['tokens']
        tokens.insert_one({'token':token,'complete_token':complete_token})
        self.client.admin.add_user(user, token, roles=[{'role':'readWrite','db':db_name}])
        return token

    def create_session(self,user,password,db_name,vr_token):

        token = self.create_token(user,db_name) # Create token that identifies the user

        if db_name in self.client.list_database_names():
            if self.user_exists(user,db_name):
                print('Entering existing database.')
                return 'vrdata.viarezo.fr', token
            else:
                print('This name is already used.')
                return None 
        else:
            from datetime import datetime
            info = { 'created on': str(datetime.utcnow()), 'admin':user }

            new_db = self.client[db_name]
            metadata = new_db['metadata'] 
            x = metadata.insert_one(info)

            if not self.user_exists(user,db_name):
                self.create_user(user,token,db_name)
        
            return 'vrdata.viarezo.fr', token

    def create_token(self,user,db_name):
        from datetime import datetime, timedelta

        JWT_SECRET = self.admin_password # change this to a random logged 16-digits secret
        JWT_ALGORITHM = 'HS256'
        JWT_EXP_DELTA_SECONDS = 20

       # selected = self.vrdata['users'].find_one({'user':user})

        payload = {
            'user': user,
            'exp': str(datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS))
        }

        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        return self.refresh_token(user,jwt_token,db_name)



    


        