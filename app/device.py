import api.apiros as apiros
import api.api as api

class Device():
    def __init__(self, devIp, devUsername, devPass):
        """Initialises device object"""
        self.sk=apiros.open_socket(devIp, 8729, True)
        """Sets device socket"""
        self.apiros=apiros.ApiRos(self.sk)
        """Sets device ApiRos"""
        self.apiros.login(devUsername, devPass)
        """Performs ApiRos login"""
        self.ip=devIp
        """Sets device IP"""
        self.api=api.Api(self)
        """Sets device Api"""
        self.name=self.api.getDevName()
        """Sets device name"""

    def getApiros(self):
        """Returns ApiRos"""
        return self.apiros
    
    def getDevIp(self):
        """Returns device IP"""
        return self.ip
    
    def getDevName(self):
        """Returns device name"""
        return self.name