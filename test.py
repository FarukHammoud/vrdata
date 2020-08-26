import vrdata
db1 = vrdata.connect('db1')
selected = db1['metadata'].find_one()

print(selected)
