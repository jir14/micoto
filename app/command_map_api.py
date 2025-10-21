import api as API
import sys, select

class Api():
    def __init__(self, ip, username, password):
        #self.sck = API.open_socket(ip, 8729, True)
        self.sk = API.open_socket(ip, 8728, False)
        self.api = API.ApiRos(self.sk)
        self.api.login(username, password)

    def apiRead(self):
        r = select.select([self.sk, sys.stdin], [], [], None)

def main():
    api = Api("10.255.255.255", "admin", "testpass")
    sentence = []
    sentence.append("/console/inspect")
    sentence.append("=request=child")
    print(api.api.talk(sentence))
    #api.api.writeSentence(sentence)
    #print(api.apiRead())

if __name__ == '__main__':
	main()