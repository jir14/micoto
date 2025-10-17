import paramiko as ssh
import telnetlib3 as telnet
import db

class scan:
    def __init__(self, ip, username, password):
        connect = telnet.Telnet(ip)
        connect.read_until(b"Login: ")
        connect.write(username.encode('ascii') + b"\n")
        connect.read_until(b"Password: ")
        connect.write(password.encode('ascii') + b"\n")
        connect.read_until(b"[admin@BC-TEST] >")
        self.conn = connect
        self.db = db.Database("db.db")

    def init_scan(self):
        a=0
        while a < 4:
            if a%2:
                self.conn.write(b"\t")
                text = self.conn.read_until(b">").strip()
                options = []
                text = text.split(b"\r\n")
                for line in text:
                    if b"\r\r" in line:
                        continue
                    for word in line.split():
                        word = word.decode()
                        options.append(word)
            a+=1
        return self.filter(options)
     
    def scan(self, *args):
        command = ""
        for arg in args:
            command+="/"+arg
        last = args[-1]
        last = last.encode("ascii")
        command = command.encode("ascii")
        self.conn.write(command + b"\r\n")
        self.conn.write(b"\t")
        self.conn.read_until(last+b">").strip()
        self.conn.read_until(last+b">").strip()
        text = self.conn.read_until(last+b">").strip()
        options = []
        text = text.split(b"\r\n")
        for line in text:
            if b"\r\r" in line:
                continue
            for word in line.split():
                word = word.decode()
                options.append(word)

        options = self.filter(options)
        self.conn.write(b"/\r\n")
        return options

    def filter(self, options):
        out = []
        for opt in options:
            if self.db.filter(opt):
                continue
            out.append(opt)
        return out
    
    def back(self):
        self.conn.write(b".." + b"\r\n")

    def checkLength(self, options):
        if len(options) == 0:
            return False
        else:
            return True


def main():
    print("start")
    scanner = scan("10.255.255.255", "admin", "testpass")
    print("connected")
    options = scanner.init_scan()
    print("scanned")
    for opt in options:
        print("")
        print(opt.upper())
    #    scanner.scan(opt)
    #    print(scanner.scan((opt)))
        for opts in scanner.scan(opt):          
            print("-"+opts)
            for optts in scanner.scan(opt, opts):
                print("--"+optts)
            
                

if __name__ == '__main__':
	main()






# telnet - tab working
#connect = telnet.Telnet("10.255.255.255")
#connect.read_until(b"Login: ")
#print("login")
#connect.write("admin".encode('ascii') + b"\n")
#connect.read_until(b"Password: ")
#print("password")
#connect.write("testpass".encode('ascii') + b"\n")

#connect.read_until(b"[admin@BC-TEST] >")
#print("command")
#connect.write(b"\t")
#print("read")
#text = connect.read_until(b"\r\r[admin@BC-TEST] >").strip()



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