import paramiko as ssh
import telnetlib3 as telnet

# telnet - tab working
connect = telnet.Telnet("10.255.255.255")
connect.read_until(b"Login: ")
print("login")
connect.write("admin".encode('ascii') + b"\n")
connect.read_until(b"Password: ")
print("password")
connect.write("testpass".encode('ascii') + b"\n")

connect.read_until(b"[admin@BC-TEST] >")
print("command")
connect.write(b"\t")
print("read")
text = connect.read_until(b"\r\r[admin@BC-TEST] >").strip()
options = []
for line in text.split(b"\r\n"):
    for word in line.split():
        options.append(word)
options.pop()
options.pop()
options.pop(0)
options.pop(0)
print(options)




# telnet - F1 working
# 'password': 'Change password'

#connect = telnet.Telnet("10.255.255.255")
#connect.read_until(b"Login: ")
#print("login")
#connect.write("admin".encode('ascii') + b"\n")
#connect.read_until(b"Password: ")
#print("password")
#connect.write("testpass".encode('ascii') + b"\n")

#connect.read_until(b"[admin@BC-TEST] >")
#print("command")
#connect.write(b"\x1B[11~")
#print("read")
#text = connect.read_until(b"\r\r[admin@BC-TEST] >").strip()
#textOpt = []
#textOpt = text.split(b"\r\n")
#options = dict()
#for option in textOpt:
#    option = option.decode()
#    if " -- " not in option:
#        continue
#    option = option.split(" -- ")
#    options[option[0]] = option[1]
#print(options)


#client = ssh.SSHClient()
#client.set_missing_host_key_policy(ssh.AutoAddPolicy())
#client.connect('10.255.255.255', 22, "admin", "testpass")

#stdin, stdout, stderr = client.exec_command('/interface/ethernet print')
#print(stdout.read().decode())

#stdin, stdout, stderr = client.exec_command('/interface/ethernet\xf1')
#print(stdout.readlines())

#client.close()

#connect = telnet.Telnet("10.255.255.255")
#connect.read_until(b"Login: ")
#print("login")
#connect.write("admin".encode('ascii') + b"\n")
#connect.read_until(b"Password: ")
#print("password")
#connect.write("testpass".encode('ascii') + b"\n")

#connect.read_until(b"[admin@BC-TEST] >")
#print("command")
#connect.write(b"\x1B[11~")
#print("read")
#text = connect.read_until(b"\r\r[admin@BC-TEST] >")
#print(text.decode('ascii'))