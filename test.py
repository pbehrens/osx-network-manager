# from netconfig import NetConfig
# 
# 
# net = NetConfig()
# 
# config = net.getConfig()
# 
# print config


import ifcfg
import json


interfaces = ifcfg.interfaces()

for i in interfaces.keys():
    # print interfaces[i]
    
    interface = interfaces[i]
    for j in interface.keys():
        if j is not None and interface is not None:
            print j + " : " + str(interface[j])

