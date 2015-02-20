from socket import *
import select
import thread
import sys
import getopt
from socket import error as SocketError
import errno

def setup(host, port, buffer, threads):
	global epollCollection
	global sockets
	global buf
	global serverSocket
	global port
	global threads
	global dataSent
	global dataRecvd
	global listenAmt

	#init
	sockets = {}
	epollCollection = {}
	dataSent = 0
	dataRecvd = 0

	#socket setup
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serverSocket.bind(('', port))
	serverSocket.listen(listenAmt)
	serverSocket.setblocking(0)

 	print "threads: %d" % threads
 	print "port: %d" % port
 	print "buffer: %d" % buf

	print "starting loop through number of threads"
	for x in range(0, threads):
		#create an epoll object for each thread
		epoll = select.epoll()
     	epollCollection.update({x:epoll})
     	connectionCount.update({x:0})
     	thread.start_new_thread(threadFunc, (x, epollCollection[x]))

	try:
		while 1:
			clientsocket, clientaddr = serverSocket.accept()
			sockets.update({clientsocket.fileno(): clientsocket})
			clientsocket.setblocking(0)
			#find the thread with the least number of current connections this allows us to load balance among
			#the threads and reduces the chance of the worst case scenario where one thread has a disproportionate
			#amount of traffic
			threadWithLowestNumberOfConnections = min(connectionCount, key=connectionCount.get)
			epollCollection[threadWithLowestNumberOfConnections].register(clientsocket.fileno(), select.EPOLLIN)
	finally:
		serversocket.close()	


def threadFunc(threadNum, epollObj):
	buf = 1024
	while 1:
		events = epollObj.poll(-1)
		# epoll level triggered on threads collection
		for fileno, event in events:
			if event & select.EPOLLIN:
				recvSocket = sockets.get(fileno)
				data = recvSocket.recv(buf)
				print data
				recvSocket.send(data)

if __name__ == '__main__':
	setup('', 7000, 1024, 8)
