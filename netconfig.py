import re
import ifcfg
import os
import json
import subprocess
from settings import *
import time
from threading import Thread
import sqlite3

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
        self.populateInterfaces()
        active = self.getActiveInterfaces()
        for interface in active:
            if interface['device'] == WIRELESS_INTERFACE and interface['status'] == 'active':
                return True
        return False
    
    def checkEthernetOn(self):
        self.populateInterfaces()
        active = self.getActiveInterfaces()
        for interface in active:
            if interface['device'] == WIRED_INTERFACE and interface['status'] == 'active':
                return True
        return False
        
    def checkVirtualInterfacePresent(self):
        populateInterfaces()
        active = getActiveInterfaces()
        for interface in active:
            if interface['device'] != WIRELESS_INTERFACE and interface['device'] != WIRED_INTERFACE:
                return True
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


class NetworkSetup(object):
    
    def __init__(self, parser):
        self.parser = parser
        
    def up(self):
        self.interfaces = self.parser.populateInterfaces()
    
    def getWifiPowerStatus(self):
        self.up()
        status = subprocess.check_output(['networksetup', '-getairportpower', self.parser.wifiDevice])
        if status[-2:] == 'On':
            return 'on'
        elif status[-3:] == 'Off':
            return 'off'
        else:
            return 'error'
    
    def turnWifiOn(self):
        self.up()
        subprocess.call(['networksetup', '-setairportpower', self.parser.wifiDevice, 'on'])
        
        
    def turnWifiOff(self):
        self.up()
        subprocess.call(['networksetup', '-setairportpower', self.parser.wifiDevice, 'off'])
        
    def getAirportName(self):
        self.up()
        name = subprocess.check_output(['networksetup', '-getairportnetwork', self.parser.wifiDevice])
        name = name[23:]
        print name
        return name
        
    def setAirportNetwork(self, name, password):
        self.up()
        name = subprocess.check_output(['networksetup', '-setairportnetwork', self.parser.wifiDevice, name, password])
        print name
        if name[0:1] == 'F':
            return False
        else:
            return True
            
    def getWifiStatus(self):
        self.up()
        return self.parser.checkWifiOn()
        
    def check(self):
        self.up()
        print self.parser.wifiDevice


class NetworkDb(object):
    
    def __init__(self):
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        self.dbPath = os.path.join(scriptdir, DB)
        
        self.db = sqlite3.connect(self.dbPath)
        
    def addNetwork(self, netDict):
        print(netDict)
        if self.checkIfNew(netDict['name']):            
            netDict = self.stringDict(netDict)
            cursor = self.db.cursor()
            cursor.execute('''INSERT INTO networks (name, safe, warn, alert, disconnect) 
            VALUES (?, ?, ?, ?, ?)''', (netDict['name'], netDict['safe'], netDict['warn'], netDict['alert'], netDict['disconnect'], ))
            print "it was inserted"
            self.db.commit()
        else:
            self.update(netDict)
            
    def update(self, netDict):
        if self.checkIfNew(netDict['name']) is True:
            self.addNetwork(netDict)
        else:
            netDict = self.stringDict(netDict)            
            cursor = self.db.cursor()
            cursor.execute('''UPDATE networks SET name = ?, safe = ?, warn = ?, alert = ?, disconnect = ? WHERE name = ?;''',
            (netDict['name'], netDict['safe'], netDict['warn'], netDict['alert'], netDict['disconnect'], netDict['name']))
            self.db.commit()
        return self.booleanDict(netDict)
    
    
    def deleteNetwork(self, networkName):
          cursor = self.db.cursor()
          cursor.execute('''DELETE FROM networks WHERE name = ? ''', (networkName,))
          self.db.commit()
          
    def getNetwork(self, networkName):
        cursor = self.db.cursor()
        cursor.execute('''SELECT * FROM networks WHERE name = ? ''', (networkName,))
        result = cursor.fetchall()
        if len(result) > 0:
            return result[0]
        else:
            return False
            
    def getNetworks(self):
        cursor = self.db.cursor()
        cursor.execute('''SELECT * FROM networks''')

        allRows = cursor.fetchall()
        convertedRows = []
        for row in allRows:
            convertedRows.append(self.booleanDict({'id':row[0], 'name':row[1], 'safe':row[2], 'warn': row[3], 'alert':row[4], 'disconnect':row[5]}))
        return convertedRows
        
    def checkIfSafe(self, networkName):
        cursor = self.db.cursor()
        cursor.execute('''SELECT * FROM networks WHERE name = ? AND safe = 'True' ''', (networkName,))
        result = cursor.fetchall()
        if len(result) > 0:
            return True
        else:
            return False
            
    def checkIfNew(self, networkName):
        cursor = self.db.cursor()
        cursor.execute('''SELECT * FROM networks WHERE name = ?''', (networkName,))
        result = cursor.fetchall()
        if len(result) > 0:
            return False
        else:
            return True
        
    def checkPermissions(self, networkName):
        cursor = self.db.cursor()
        cursor.execute('''SELECT * FROM networks WHERE name = ?''', (networkName,))
        result = cursor.fetchall()
        
        networkStatus = {'name': networkName, 'safe': False, 'warn':False, 'alert': False, 'disconnect': False}
        if len(result) > 0:
            network = result[0]
            networkStatus['name'] = networkName
            if network[2] == 'True':
                networkStatus['safe'] = True
                networkStatus['disconnect'] = False
            if network[3] == 'True':
                networkStatus['warn'] = True
            if network[4] == 'True':
                networkStatus['alert'] = True
            if network[5] == 'True':
                networkStatus['disconnect'] = True
                networkStatus['safe'] = False
        else:
            self.addNetwork(networkStatus)
            
        return networkStatus
              
   
    def stringDict(self, netDict):
        for i in netDict.keys():
            if netDict[i] is True:
                netDict[i] = 'True'
            elif netDict[i] is False:
                netDict[i] = 'False'
        return netDict
                
    def booleanDict(self, netDict):
        for i in netDict.keys():
            if netDict[i] == 'True':
                netDict[i] = True
            elif netDict[i] == 'False':
                netDict[i] = False
        return netDict

    def printNetworks(self):
        print len(self.networks)
        for network in self.networks:
            print network
    
    
class NetObj(object):
    
    def __init__(self, parser):
        self.netDict = {'name':''}
        self.db = NetworkDb()
        self.setup = NetworkSetup()
        self.parser = parser
        self.wifiOn = False
        self.nameChanged = False
        self.stateChanged = False
        self.updateDb()
        self.highestState = self.getNetworkState()
                    
    def updateDb(self):
        if  self.setup.getWifiStatus() is True:
            self.wifiOn = True
            networkName =  self.setup.getAirportName()
            if networkName != self.netDict['name']:
                self.nameChanged = True
                self.netDict['name'] = networkName
            self.netDict['name'] = self.setup.getAirportName()
            networkStatus = self.db.checkPermissions(self.netDict['name'])
            self.netDict['safe'] = networkStatus['safe']
            self.netDict['warn'] = networkStatus['warn']
            self.netDict['alert'] = networkStatus['alert']
            self.netDict['disconnect'] = networkStatus['disconnect']
        else:
            self.wifiOn = False
            self.netDict = {'safe': False, 'warn': True, 'alert': False, 'disconnect':False, 'name': ''}
        print 'before update'
        print self.netDict
        self.db.update(self.netDict)
        print 'after update'
        updatedNetwork = self.db.getNetwork(self.netDict['name'])
        return updatedNetwork
        
    def checkIfStatusSelected(self):
        if self.netDict['safe']  is False and self.netDict['warn']  is False and self.netDict['alert'] is False and self.netDict['disconnect']  is False:
            self.warn = True
            return False
        else:
            return True
            
    def updateState(self, state, value):
        print "change " + state + " to " + str(value)
        if self.netDict['safe'] is False and state == 'safe':
            self.netDict['safe'] = value
        if self.netDict['disconnect'] is False and state == 'disconnect':
            self.netDict['disconnect'] = value
            
        if self.netDict['safe'] is True and state == 'disconnect' and value is True:
            self.netDict['safe'] = False
            self.netDict['disconnect'] = True
        elif self.netDict['disconnect'] is True and state == 'safe' and value is True:
            self.netDict['disconnect'] = False
            self.netDict['safe'] = True
        else:
            self.netDict[state] = value
        
        self.stateChanged = True
        print 'after state change'
        print self.netDict
        
    def checkChanged(self):
        changes = False
        if self.nameChanged is True:
            self.networkChanged = False
            changes = True
        if self.stateChanged is True:
            self.stateChanged = False
            changes = True
        return changes
        
    def getNetworkState(self):
        highestState = 'safe'
        if self.netDict['safe'] is True:
            highestState = 'safe'
        if self.netDict['warn'] is True:
            highestState = 'warn'
        if self.netDict['alert'] is True:
            highestState = 'alert'
        if self.netDict['disconnect'] is True:
            highestState = 'disconnect'
        self.highestState = highestState
        return highestState

# class StateController(object):
#     
#     def __init__(self, time):
#         self.time = time
#         self.db = NetworkDb()
#         self.setup = NetworkSetup()      
#         self.parser = InterfaceParser()
#         self.netObj = NetObj()        
#         self.currentIcon = ''
#         self.currentConnection = ''
#         self.controlLoop()
#         
#     def controlLoop(self):
#         print self.netObj.netDict
#         if self.netObj.checkChanged() is True:
#             #some sort of change occured
#             self.netObj.updateDb()
#         print self.determineAction(self.netObj.getNetworkState())
# 
#     
#     
#     def determineAction(self, state):
# # if safe, ensure green icon, network is connected
#         if state == 'safe':
#             self.verifyIcon('green')
#             self.verifyConnection('on')
#         
#         # if warning, display yellow icon, keep connection alive
#         if state == 'warn':
#             self.verifyIcon('yellow')
#             self.verifyConnection('on')
#         #     if alert state present an nalert message, display the red icon and keep connection alive
#         if state == 'alert':
#             self.verifyIcon('red')
#             self.alertMessage()
#             self.verifyConnection('on')
#             
#         if state == 'disconnect':
#             self.verifyIcon('x')
#             self.verifyConnection('off')
#             # self.alertMessage()
#             
#         
#     
#     def verifyIcon(self, neededIcon):
#         if neededIcon != self.currentIcon:
#             self.currentIcon = neededIcon
#             self.updateIcon()
#             
#     def updateIcon(self):
#         print "icon: " + self.currentIcon
#             
#     def verifyConnection(self, neededConnection):
#         if neededConnection != self.currentConnection:
#             verified = self.alterConnection(neededConnection)
#             return verified
#         return true
# 
#     def alterConnection(self, neededConnection):
#         if neededConnection == 'off':
#             self.setup.turnWifiOff()
#             if self.setup.getWifiPowerStatus() == 'off':
#                 return True
#         elif neededConnection == 'on':
#             self.setup.turnWifiOn()
#             if self.setup.getWifiPowerStatus() == 'on':
#                 return True
#             return True
#         else:
#             #do nothing some error occured
#             print "error"
#         return False
#             
# class NetworkCommand(object):
#     def __init__(self, interface, command,):
        
            
class NetworkStatusThread(Thread):
    def __init__(self, uiUpdateCallback, interfaceUpdateCallback, networkCommand, interval):
        Thread.__init__(self)
        self.callback = callback
        self.parser = InterfaceParser()
        self.interval = interval

    def collectNetworkData(self):
        return self.parser.populateInterfaces()
        
    def run(self):
        data = "hello"
        self.interfaceUpdateCallback(self.collectNetworkData())
        time.sleep(interval)


# db = NetworkDb()
# 
# netDict = {}
# netDict['name'] = 'jeffrey2' 
# netDict['safe'] = True
# netDict['warn'] = True
# netDict['alert'] = False
# netDict['disconnect'] = False
# # 
# db.addNetwork(netDict)
# # 
# # 
# nets = db.getNetworks()
# 
# #     
# # safe = safenets.checkIfSafe('bartertown')
# 
# stateControl = StateController()
# stateControl.updateState('safe', False)
# stateControl.updateState('warn', True)
# state = stateControl.updateDb()
# 
# stateControl.updateState('disconnect', True)
# stateControl.updateState('warn', True)
# 
# state = stateControl.updateDb()
# 
# print "count is " + str(len(nets)) + " networks "
# 



# setup = NetSetup()
# 
# setup.check()
# 
# success = setup.setAirportNetwork('bartertown', 'hamb762h6')
# 
# if success:
#     print 'connected well'
# else:
#     print 'didnt connect'
