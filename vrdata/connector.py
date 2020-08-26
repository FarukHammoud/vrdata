class Connector:
    
    def __new__(self,db_name,username = None,password = None):
        self.db_name = db_name
        self.username = username
        self.password = password

        if self.username is None:
            self.username = input('username: ')

        if self.password is None:
            self.password = input('password: ')

        import requests, json

        url = 'http://vrdata.viarezo.fr/auth'
        login_info = {'username':self.username,'password':self.password}
        x = requests.post(url, json = login_info)

        print(x.text)
        result = x.json()

        if result['verified'] == '1':
            
            server = result['server']
            token = result['token'] 

            import pymongo
            client = pymongo.MongoClient(server,username=self.username,password=token,authSource=db_name)
            return client[db_name]
        else:
            print('Wrong Credentials. Aborting.')
            return None

