import re
import ifcfg
import json
from subprocess import call
from settings import *

class InterfaceParser(object):
    
    def __init__(self):
        self.foo = ""
        self.interfaces = []
        self.wifiDevice = None
        self.wiredDevice = None
        self.virtual = []
        self.other = []
        self.activeInterfaces = []
        self.inactiveInterfaces = []
    def turnWifiOn(self):
        foo = ""
    def turnWifiOff(self):
        foo = ""
    def getWifiState(self):
        foo = ""
    def getWifiNetwork(self):
        foo = ""
        
    def getWifiDevice(self):
        self.populateInterfaces()
        return self.wifiDevice['device']
        
    def getWiredDevice(self):
        self.populateInterfaces()
        return self.wiredDevice['device']
        
    def getWifi(self):
        self.populateInterfaces()
        for interface in  self.interfaces:
            if interface['device'] == WIRELESS_INTERFACE:
                return interface
            else:
                return None
        
                   
    def populateInterfaces(self):
        newInterfaces = ifcfg.interfaces()
        self.interfaces = []
        self.virtual = []
        self.activeInterfaces = []
        self.inactiveInterfaces = []
        
        for i in newInterfaces.keys():
            # get each interface one by one
            interface = newInterfaces[i]
            device = interface['device']
            self.markStatus(interface)
            if device == WIRELESS_INTERFACE:
                self.wifiDevice = WIRELESS_INTERFACE
                self.wifi = interface['device']
            elif device == WIRED_INTERFACE:
                self.wiredDevice = WIRED_INTERFACE
                self.wired = interface
            elif device.find('en') != -1:
                self.virtual.append(interface)
            else:
                self.other.append(interface)
                        
                        
                        
            self.interfaces.append(newInterfaces[i])        

    def markStatus(self, interface):
        if interface['status'] == 'active':
            self.activeInterfaces.append(interface)
        else:
            self.inactiveInterfaces.append(interface)
            
    def getActiveInterfaces(self):
        self.populateInterfaces()
        active = []
        for interface in self.interfaces:
            if interface['status'] == 'active':
                active.append(interface)
        return active
        
    def checkWifiOn(self):
        populateInterfaces()
        active = getActiveInterfaces()
        for interface in active:
            if interface['device'] == WIRELESS_INTERFACE and interface['status'] == 'active':
                return True
            else:
                return False
    
    def checkEthernetOn(self):
        populateInterfaces()
        active = getActiveInterfaces()
        for interface in active:
            if interface['device'] == WIRED_INTERFACE and interface['status'] == 'active':
                return True
            else:
                return False
                
    def checkVirtualInterfacePresent(self):
        populateInterfaces()
        active = getActiveInterfaces()
        for interface in active:
            if interface['device'] != WIRELESS_INTERFACE and interface['device'] != WIRED_INTERFACE:
                return True
            else:
                return False
        
    def printInterfaceData(self):
        print 'active interfaces'
        print self.activeInterfaces
        
        print 'inactive interfaces'
        print self.inactiveInterfaces
        
        print 'wireless'
        print self.wifi
        
        print ' wired'
        print self.wired
        
        print 'virtual interfaces'
        print self.virtual
        
        print ' all interfaces'
        print self.interfaces

class NetSetup(object):
    
    def __init__(self):
        self.parser = InterfaceParser()
        
    def up(self):
        self.interfaces = self.parser.populateInterfaces()
    
    def getWifiPowerStatus(self):
        self.up()
        call(['networksetup', '-getairportpower', self.parser.wifiDevice])
    
    def turnWifiOn(self):
        self.up()
        call(['networksetup', '-setairportpower', self.parser.wifiDevice, 'on'])
        
        
    def turnWifiOff(self):
        self.up()
        call(['networksetup', '-setairportpower', self.parser.wifiDevice, 'off'])
        
    def check(self):
        self.up()
        print self.parser.wifiDevice


setup = NetSetup()

setup.check()