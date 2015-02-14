from socket import *
import select
import threading

connectionCount = {}

def setup(host, port, buffer, threads):
	epollCollection = []
	addr = (host, port)
 	serversocket = socket(AF_INET, SOCK_STREAM)


	for x in range(0, threads):
		#create an epoll object for each thread
		epoll = select.epoll()
     	epollCollection.insert(x, epoll)
     	connectionCount.update({x:0})
     	thread(x, epoll)

	serversocket.bind(addr)
	serversocket.listen(10000)

	try:
		while 1:
			clientsocket, clientaddr = serversocket.accept()
			clientsocket.setblocking(0)
			threadWithLowestNumberOfConnections = min(connectionCount, key=connectionCount.get)

			epollCollection[threadWithLowestNumberOfConnections].register(clientsocket.fileno(), select.EPOLLIN)


	finally:
		serversocket.close()	


def thread(threadNum, epollObj):
	buf = 1024
	while 1:
		events = epollObj.poll(-1)
		# epoll level triggered on threads collection
		for fileno, event in events:
			if event & select.EPOLLIN:
				data = fileno.recv(buf)
				print buff
				fileno.send(data)
		# on unblock call messaging (read from socket, echo back)

#def accept:

#def messaging:




if __name__ == '__main__':
	setup('localhost', 7000, 1024, 8)
