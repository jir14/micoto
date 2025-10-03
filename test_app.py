from app.db_crypto import DBConn

db = DBConn("db.db", "pes les")

db.insert("testName", "10.255.255.255", "admin", "testpass")

#print(db.selectAll())

for row in db.selectAll():
    print(row)

#for row in db.query("SELECT * FROM devices"):
#    print(row)

