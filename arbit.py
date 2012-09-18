#!/usr/bin/python

import thread
import time



def print_time(threadName, delay):
    count = 0
    while count<5:
        time.sleep(delay)
        count+=1
        if count == 5:
            break;
        print "%s: %s" % ( threadName, time.ctime(time.time()) )

try:
    thr = []
    t_1 = thread.start_new_thread(print_time, ("thread-1", 2,) )
    thr.append(t_1)
    t_2 = thread.start_new_thread(print_time, ("thread-2", 4,) )
    thr.append(t_2)

except:
    print "error occured, unable to start thread"

for t in thr:
    print t
    
while 1:
    pass
    
    
    

