import api.apiros as apiros
import api.api as api
import time

class Device():
    def __init__(self, devIp, devUsername, devPass):
        self.sk=apiros.open_socket(devIp, 8729, True)
        self.apiros=apiros.ApiRos(self.sk)
        self.apiros.login(devUsername, devPass)
        self.ip=devIp
        self.api=api.Api(self)
        self.name=self.api.getDevName()

    def getApiros(self):
        return self.apiros
    
    def getDevIp(self):
        return self.ip
    
    def getDevName(self):
        return self.name