import api.apiros as apiros
import api.api as api

class Device():
    def __init__(self, devIp, devUsername, devPass):
        self.sk=apiros.open_socket(devIp, 8729, True)
        #self.sk=apiros.open_socket(devIp, 8728, False)
        print(devIp)
        print(type(devIp))
        self.apiros=apiros.ApiRos(self.sk)
        # add login check!!!
        self.apiros.login(devUsername, devPass)
        self.ip=devIp
        self.api=api.Api(self)
        self.name=self.api.getDevName()
        pass

    def getApiros(self):
        return self.apiros
    
    def getDevIp(self):
        return self.ip
    
    def getDevName(self):
        return self.name