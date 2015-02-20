from socket import *
import select
import thread
import sys
import getopt
from socket import error as SocketError
import errno

def setup():
	global epollCollection
	global sockets
	global buf
	global serverSocket
	global port
	global threads
	global dataSent
	global dataRecvd
	global listenAmt
	global connectionCount

	#init
	sockets = {}
	epollCollection = {}
	connectionCount = {}
	dataSent = 0
	dataRecvd = 0

	#socket setup
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serverSocket.bind(('', port))
	serverSocket.listen(listenAmt)
	#serverSocket.setblocking(0)

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
			epollCollection[threadWithLowestNumberOfConnections].register(clientsocket, select.EPOLLIN)
	finally:
		serverSocket.close()	


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

def main(argv):
    global port
    global buf
    global threads
    global listenAmt

    try:
        opts, args = getopt.getopt(argv, "t:l:p:b:h",["threads=", "listenAmt=", "port=", "buffer=", "help"])
    except getopt.GetoptError:
        #usage()
        sys.exit(2)
    
    if len(sys.argv) < 3:
        print 'leveltriggered.py -t <threads> -l <listenAmt> -p <port> -b <bufferSize>'
        sys.exit()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'leveltriggered.py -t <threads> -l <listenAmt> -p <port> -b <bufferSize>'
            sys.exit()
            port = int(arg)
        elif opt in ("-t", "--threads"):
            threads = int(arg)
        elif opt in ("-l", "--listenAmt"):
            listenAmt = int(arg)
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-b", "--buffer"):
            buf = int(arg)

if __name__ == '__main__':
	main(sys.argv[1:])
	setup()
