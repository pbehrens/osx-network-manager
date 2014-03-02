import threading
import time
class stringRepeater(threading.Thread):
    def __init__(self, workQueue, count):
        threading.Thread.__init__(self)
        self.workQueue = workQueue
        self.repeatCount = count

    def run(self):
        while True:
            teststring = self.workQueue.get()
            for i in range(self.repeatCount):
                print teststring
                time.sleep(2)

    def setCount(self, newcount):
        self.repeatCount = newcount