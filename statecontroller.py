from netconfig import *

class StateController(object):
    
    def __init__(self, time):
        self.interval = time
        self.db = NetworkDb()
        self.parser = None
        self.netObj = NetObj()        
        self.currentIcon = ''
        self.currentConnection = ''
        self.controlLoop()
        NetworkStatusThread(self.initParser, 0).start()
        self.refresh = True
        
    
    def controlLoop(self):
        print self.netObj.netDict
        if self.netObj.checkChanged() is True:
            #some sort of change occured
            self.netObj.updateDb()
        print self.determineAction(self.netObj.getNetworkState())
        
    def stopRefresh(self):
        self.refresh = False
        
    def startRefresh(self):
        self.refresh = True
        NetworkStatusThread(self.initParser, 0).start()
        
    def initParser(self, parser, interval):
        self.parser = parser
        self.controlLoop()
        NetworkStatusThread(self.maintainNetworkStatus, self.interval).start()
            
    def maintainNetworkStatus(self, parser, interval):
        self.parser = parser
        self.controlLoop()
        if refresh is True
            NetworkStatusThread(self.maintainNetworkStatus, self.interval).start()
        
        
    def determineAction(self, state):
# if safe, ensure green icon, network is connected
        if state == 'safe':
            self.verifyIcon('green')
            self.verifyConnection('on')
        
        # if warning, display yellow icon, keep connection alive
        if state == 'warn':
            self.verifyIcon('yellow')
            self.verifyConnection('on')
        #     if alert state present an nalert message, display the red icon and keep connection alive
        if state == 'alert':
            self.verifyIcon('red')
            self.alertMessage()
            self.verifyConnection('on')
            
        if state == 'disconnect':
            self.verifyIcon('x')
            self.verifyConnection('off')
            # self.alertMessage()
            
        
    
    def verifyIcon(self, neededIcon):
        if neededIcon != self.currentIcon:
            self.currentIcon = neededIcon
            self.updateIcon()
            
    def updateIcon(self):
        print "icon: " + self.currentIcon
            
    def verifyConnection(self, neededConnection):
        if neededConnection != self.currentConnection:
            verified = self.alterConnection(neededConnection)
            return verified
        return true

    def alterConnection(self, neededConnection):
        if neededConnection == 'off':
            self.setup.turnWifiOff()
            if self.setup.getWifiPowerStatus() == 'off':
                return True
        elif neededConnection == 'on':
            self.setup.turnWifiOn()
            if self.setup.getWifiPowerStatus() == 'on':
                return True
            return True
        else:
            #do nothing some error occured
            print "error"
        return False