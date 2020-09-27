import socket
import argparse
import queue
from threading import *



threads = 300
que = queue.Queue()
lock = Lock()
none = 0
def scan(port):

	try:
		Sock = socket.socket()
		Sock.connect((host,port))
	except:
		with lock:
			none = 1



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

    host = "192.168.1.47"


    ports = [ p for p in range(1, 65535)]

    main(host, ports)


