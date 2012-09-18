import threading
import time
import logging

class peterson(threading.Thread):

    counter = 10
    logging.basicConfig(level=logging.DEBUG, format='[%(threadName)s, %(message)s]')
    B = [0]*2
    
    def __init__(self, threadName):
        self.threadName = threadName
        threading.Thread.__init__(self)
        
    def run(self):
        logging.debug('starting')
        time.sleep(2)
        while peterson.counter:
            threadlock.acquire()
            enterCS()
            threadlock.release()
            peterson.counter-=1
        
def enterCS():
    logging.debug('now in cs...')
  
        

threadlock = threading.Lock()

p_1 = peterson('process 1')
p_2 = peterson('process 2')

p_1.start()
p_2.start()

while 1:
    pass
