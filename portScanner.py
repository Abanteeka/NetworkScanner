import socket
import sys
import time
import threading
from queue import Queue

if len(sys.argv) == 2:
    # target = input('Enter the host to be scanned: ')
    # translate hostname to IPv4
    target = socket.gethostbyname(sys.argv[1])
    print('Starting scan on host: ', target)
else:
    print("Invalid amount of Argument")

socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()


def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((target, port))
        with print_lock:
            print(port, 'is open')
        con.close()
    except:
        pass


def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()


q = Queue()
startTime = time.time()

for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for worker in range(1, 500):
    q.put(worker)

q.join()
print('Time taken:', time.time() - startTime)
