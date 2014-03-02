import Queue
import threading
import urllib2
from netconfig import *
from threading import Thread
import time
from statecontroller import StateController
# 
# 
# 
menu = {}
menu['1']="Add Student." 
menu['2']="Delete Student."
menu['3']="Find Student"
menu['4']="Exit"


# Start thread at interval

stateController = StateController()

while True: 
    options=menu.keys()
    options.sort()
    for entry in options: 
        print entry, menu[entry]

    selection=raw_input("Please Select:") 
    if selection =='1': 
        print "add" 
    elif selection == '2':
        thread = NetworkStatusThread(30)
        thread.start()
        thread.join()
        thread.err 
        print "delete"
    elif selection == '3':
        print "find" 
    elif selection == '4': 
        break
    else: 
        print "Unknown Option Selected!" 


class Manager():
    def runThread(self, interval):
        NetworkStatusThread(self.on_thread_finished, interval).start()
        
    def 

    def on_thread_finished(self, data):
        print "on_thread_finished:", data
        NetworkStatusThread(self.on_thread_finished).start()
        
m = Manager()
m.Test() # prints "on_thread_finished: hello"