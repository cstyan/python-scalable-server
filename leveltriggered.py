import socket, select

connectionCount = {}

def setup(host, port, buffer, threads):
	epollCollection = []
	

	addr = (host, port)
 
    serversocket = socket(AF_INET, SOCK_STREAM)


     for x in range(threads):
     	#create an epoll object for each thread
     	epoll = select.epoll
     	epollCollection[x] = epoll
     	connectionCount.update({x:0})
     	thread(threadNum, epoll)
 
    serversocket.bind(addr)
 
    serversocket.listen(10000)

    try:
    	while 1:
    		clientsocket, clientaddr = serversocket.accept()

    		threadWithLowestNumberOfConnections = min(connectionCount, key=connectionCount.get)

    		epollCollection[threadWithLowestNumberOfConnections].register(clientsocket.fileno(), select.EPOLLIN)
    	

    finally:
   
    	serversocket.close()	


def thread(threadNum, epollObj):
	epoll = select.epoll()
	epoll.register()
	while 1:
		events = epoll.poll(5)
		# epoll level triggered on threads collection

		# on unblock call messaging (read from socket, echo back)

def accept:

def messaging:




if __name__ == '__main__':


