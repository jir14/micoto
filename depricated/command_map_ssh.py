import paramiko

class scan:
    def __init__(self, ip, username, password):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(ip, 22, username, password)
        

def main():
    ssh = scan("10.255.255.255", "admin", "testpass")
    stdin, stdout, stderr = ssh.client.exec_command('/console/inspect request=child')
    text = stdout.read().split(b"\r\n")
    for t in text:    
        print(t.strip())

if __name__ == '__main__':
	main()