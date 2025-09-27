from db_crypto import DBConn

db = DBConn("db.db", "pes")

db.dbInsert("testName", "10.255.255.254", "admin", "testpass")


for row in db.dbQuery("SELECT * FROM devices"):
    print(row)