from app.db.db_crypto import DBConn

db = DBConn("devices.db", "pero")

db.insert("testName", "10.255.255.255", "admin", "testpass")

#print(db.selectAll())

for row in db.selectAll(True):
    print(row)
