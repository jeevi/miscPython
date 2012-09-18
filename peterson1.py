import threading
import time
import logging

class Peterson(threading.Thread):
    
    counter = 10
    logging.basicConfig(level=logging.DEBUG, format='[%(threadName)s, %(message)s]')
    
    B = [0]*2
    turn = 9
    
    def __init__(self, threadName, index):
        self.threadName = threadName
        self.index = index
        threading.Thread.__init__(self)
        
    def run(self):
        logging.debug('is starting ...')
        time.sleep(2)
        while Peterson.counter:
            B[self.index] = 1
            x = !self.index
            turn = x
            while(B[x]==1 and turn == x):
                    logging.debug('waiting ... ')
            enterCS()
            B[self.index] = 0
            Peterson.counter -= 1

def enterCS():
    logging.debug('executing in CS ...')
    logging.debug('exiting CS ...')
    


t0 = Peterson('process-0', 0)
t1 = Peterson('process-1', 1)

t0.start()
t1.start()


            
