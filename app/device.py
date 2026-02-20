import apiros as apiros

class device():
    def __init__(self, devName, devIp, devUsername, devPass):
        self.sk=apiros.open_socket(devIp, 8729, True)
        #self.sk=apiros.open_socket(devIp, 8728, False)
        self.apiros=apiros.ApiRos(self.sk)
        # add login check!!!
        self.apiros.login(devUsername, devPass)
        self.ip=devIp
        self.name=devName
        pass

    def getApiros(self):
        return self.apiros
