import threading
import time

def worker():
    print threading.currentThread().getName() + " is working..."
    time.sleep(1)
    
t = threading.Thread(target=worker)
u = threading.Thread(name="i gotta name", target=worker)

t.run()
u.start()
