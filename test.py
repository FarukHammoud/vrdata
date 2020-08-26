import vrdata
vrdb = vrdata.connect('vrdata')
selected = vrdb['users'].find_one({'user':'2019hammoudf'})

print(selected['password'])
