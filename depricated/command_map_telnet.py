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
        self.ip = ip
        self.username = username
        self.password = password
        self.db = db.Database("db.db")

    def init_scan(self):
        a=0
        while a < 4:
            if a%2:
                self.conn.write(b"\t")
                text = self.conn.read_until(b">").strip()
                options = []
                text = text.split(b"\r\n")
                options = self.iterate(text)
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
        options = self.iterate(text)
        options = self.filter(options, command.decode())
        self.conn.write(b"/\r\n")
        return options

    def filter(self, options, command=""):
        out = []
        for opt in options:
            if self.db.filterWords(opt):
                self.db.insertRoutes(command+"/"+opt)
                continue
            if self.db.filterOptions(opt):  
                continue
            out.append(opt)
        return out
        
    def scanAll(self):
        print("start")
        scanner = scan(self.ip, self.username, self.password)
        print("connected")
        options = scanner.init_scan()
        scanner.db.clearTable("routes")
        for opt in options:
            print("")
            print(opt.upper())
            for opts in scanner.scan(opt):          
                print("-"+opts)
                for optts in scanner.scan(opt, opts):
                    print("--"+optts)
                    for opttts in scanner.scan(opt, opts, optts):
                        print("---"+opttts)
                        for optttts in scanner.scan(opt, opts, optts, opttts):
                            print("---"+optttts)
                            for opttttts in scanner.scan(opt, opts, optts, opttts, optttts):
                                print("---"+opttttts)
                                for optttttts in scanner.scan(opt, opts, optts, opttts, optttts, opttttts):
                                    print("---"+optttttts)
        for route in self.db.selectAllRoutes():
            self.options(route)
        print("scanned")
        return
    
    def iterate(self, text):
        output = []
        for line in text:
            if b"\r\r" in line:
                continue
            for word in line.split():
                word = word.decode()
                output.append(word)
        return output
    
    def options(self, command):
        command = command.encode("ascii")
        self.conn.write(command + b" \t")
        self.conn.read_until(b">").strip()
        text = self.conn.read_until(b">").strip().decode()
        text = text.split()
        text.pop()
        text.pop()
        text.pop(0)
        self.db.insertOptions(command, text)
        for t in len():
            self.conn.write(b"")
            print(self.conn.read_until(b">").strip())
        self.conn.read_until(b">").strip()
        return 

    
def main():
    test = scan("10.255.255.255", "admin", "testpass")
    #test.scanAll()
    #for route in test.db.selectAllRoutes():
    #        if test.db.filterOptions(route[0]) in route:
    #            continue
    #        print(route[0])
    #        test.options(route[0])
    test.options("/caps-man/aaa/edit")
    print("pes")
    test.options("/caps-man/aaa/export")
    print("les")
    #test.db.insertOptions("/caps-man/datapath", test.options("/caps-man/datapath/add"))

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