from socket import *
import select
import thread

connectionCount = {}
sockets = {}

def setup(host, port, buffer, threads):
	epollCollection = []
	addr = (host, port)
 	serverSocket = socket(AF_INET, SOCK_STREAM)

	print "starting loop through number of threads"
	for x in range(0, threads):
		#create an epoll object for each thread
		epoll = select.epoll()
     	epollCollection.insert(x, epoll)
     	connectionCount.update({x:0})
     	thread.start_new_thread(threadFunc, (x, epollCollection[x]))

	#should these calls not be before the thread creation?
	serversocket.bind(addr)
	serversocket.listen(2)
	print "server socket set up"

	try:
		while 1:
			print "test 1"
			clientsocket, clientaddr = serversocket.accept()
			sockets.update({clientsocket.fileno(): clientsocket})
			print "after"
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
				data = sockets.get(fileno).recv(buf)
				print data
				fileno.send(data)
		# on unblock call messaging (read from socket, echo back)

#def accept:

#def messaging:




if __name__ == '__main__':
	setup('192.168.0.13', 7000, 1024, 8)
