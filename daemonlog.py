import threading
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s, %(threadName)-10s, %(message)s]',)

def daemo():
    logging.debug('starting')
    time.sleep(2)
    logging.debug('exiting')
    
def nondaemo():
    logging.debug('starting')
    time.sleep(1)
    logging.debug('exiting')
    
t = threading.Thread(name='daemon thread ', target=daemo)
t.setDaemon(True)
u = threading.Thread(name='normal thread1 ', target=nondaemo)
v = threading.Thread(name='normal thread1 ', target=nondaemo)

t.start()
u.start()
v.start()


t.join()
u.join()
v.join()


