import apiros as API

class Api():
    def __init__(self, ip, username, password, db=None):
        self.sk = API.open_socket(ip, 8729, True)
        #self.sk = API.open_socket(ip, 8728, False)
        self.api = API.ApiRos(self.sk)
        self.api.login(username, password)
        self.db = db

    def parser(self, reply):
        for re in reply:
            if re[0]=="!re":
                for r in re[1].keys():
                    print(r.replace("=",""), re[1][r])
        return

    def printDir(self, dirID):
        sentence = []
        sentence.append(self.db.printDirPath(dirID)+"/print")
        out = self.api.talk(sentence)
        return out