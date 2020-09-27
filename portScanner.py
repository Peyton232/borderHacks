import socket
import argparse
import queue
from threading import *



threads = 300
que = queue.Queue()
lock = Lock()
def scan(port):
	
	try:
		Sock = socket.socket()	
		Sock.connect((host,port))
	except:
		with lock:
			pass

	else:
		with lock:
			print(f"{host}:{port} is open")			
	
	finally:
		Sock.close()



def threadx():
	global que
	while True:
		work = que.get()
		scan(work)
		que.task_done()		

	
			
def main(host,ports):
	global que
	for i in range(threads):
		i = Thread(target=threadx)
		i.daemon = True
		i.start()

	for worker in ports:
		que.put(worker)


	que.join()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple port scanner")
    parser.add_argument("host", help="Host to scan.")
    parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="Port range to scan, default is 1-65535 (all ports)")
    args = parser.parse_args()
    host, port_range = args.host, args.port_range

    start_port, end_port = port_range.split("-")
    start_port, end_port = int(start_port), int(end_port)

    ports = [ p for p in range(start_port, end_port)]

    main(host, ports)


