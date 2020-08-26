import vrdata
vrdb = vrdata.connect('admin')
selected = vrdb['users'].find()

print(selected)
