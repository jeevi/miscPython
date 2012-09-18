import threading
import time
import logging

B = [0]*2
turn = 9
    

class Peterson(threading.Thread):
    
    counter = 10
    
    logging.basicConfig(level=logging.DEBUG, format='[%(threadName)s, %(message)s]')
        
    def __init__(self, index):
        self.index = index
        threading.Thread.__init__(self)
        
    def run(self):
    
        logging.debug('is starting ...')
        B[self.index] = 1
        turn =  self.index

        #print  threading.currentThread().getName() + " " + str(B[not self.index])
        #print threading.currentThread().getName()+ " " + str(turn)

        while(B[not self.index] is 1 and turn is self.index ):
          
            logging.debug('waiting ... ')
        enterCS()
        B[self.index] = 0
        #print threading.currentThread().getName() + " " +str(B[self.index])


def enterCS():
    logging.debug('executing in CS ...')
    logging.debug('exiting CS ...')
    


t0 = Peterson(0)
t1 = Peterson(1)

t0.start()
t1.start()


            
