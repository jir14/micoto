import routeros_api
import app.db

connection = routeros_api.RouterOsApiPool(
    '10.255.255.255',
    username='admin',
    password='testpass',
    plaintext_login=True,
    use_ssl=True,
    ssl_verify=False,
    ssl_verify_hostname=False,
)
api = connection.get_api()

db = app.db.Database("./app/db.db")

list = api.get_resource("/caps-man/rates")
for rec in list.get():
    print(rec)

#for route in db.selectAllRoutes():
#    list = api.get_resource(route)
#    for rec in list.get():
#        print(rec)

