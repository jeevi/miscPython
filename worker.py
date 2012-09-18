import threading
import time

def worker():
   print"in worker def"
   time.sleep(2)
   
   
t = threading.Thread(target=worker)

t.start()

