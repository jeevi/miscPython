#!usr/bin/python

import threading
import time

exitFlag = 0

class mythread(threading.Thread):

    def __init__(self, threadName, delay):
        
            self.threadName = threadName
            self.delay = delay
            threading.Thread.__init__(self)
            
    def run(self):
            
            print "starting:" + self.threadName
            print_time(self.threadName, self.delay, 5)
            print "exiting " + self.name
            
def print_time(threadName, delay, counter):
    
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        print "%s %s" %(threadName, time.ctime(time.time()))
        counter-=1
        
t_1 = mythread("thread-1", 2)
t_2 = mythread("thread-2", 2)

t_1.start()
t_2.start()

while not t_1.isAlive():
    if not t_2.isAlive():
        exitFlag = 1
    pass
    
print "exiting the main thread"

      
