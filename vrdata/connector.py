class Connector:
    
    def __init__(self,db_name,username = None,password = None):
        self.db_name = db_name
        self.username = username
        self.password = password
        
        if self.username is None:
            self.username = input('username: ')

        if self.password is None:
            self.password = input('password: ')

        import requests

        url = 'http://vrdata.viarezo.fr/auth'
        myobj = {'username':self.username,'password':self.password}

        x = requests.post(url, data = myobj)

        print(x.text)
        
        self.token = None
    def insert(self,document):
        pass
    def find(self,query,scope):
        pass