from socket import *
import select
import thread
import sys

buf = 2048
sockets = {}
epoll = select.epoll()

#initial setup, including server socket and registration with the epoll object
def setup(host, port, buffer, threads):
    #access all the globals
    global buf
    global serverSocket
    global epoll
    global sockets

    buf = buffer
    #socket setup
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    epoll.register(serverSocket, select.EPOLLIN | select.EPOLLET)
    #add the server socket to the global sockets collection
    sockets.update({serverSocket.fileno(): serverSocket})
    #start the threads, they all have access to the global epoll object and all sockets
    for x in range(0, threads):
        thread.start_new_thread(threadFunc, ())
        print "thread created"

    serverSocket.bind(('', port))
    serverSocket.listen(10)
    threadFunc()

#main driver for each thread
def threadFunc():
    global serverSocket
    global epoll
    print " starting infinite loop"
    while 1:
        #epoll edge triggered on the global epoll object
        events = epoll.poll(-1)
        for fileno, event in events:
            #accept event
            if fileno == serverSocket.fileno():
                acceptHandler()
            #data event
            elif event & select.EPOLLIN:
                dataHandler(fileno)

#handle the incomming accept event
def acceptHandler():
    #access globals
    global sockets
    global serverSocket

    clientSocket, clientAddr = serverSocket.accept()
    #set non-blocking mode
    clientSocket.setblocking(0)
    #add the new client socket to the global collection
    sockets.update({clientSocket.fileno(): clientSocket})
    epoll.register(clientSocket.fileno(), select.EPOLLIN | select.EPOLLET)
    print "client connected!"

#handle the incomming data event
def dataHandler(fileno):
    #access globals
    global sockets
    global buf

    clientSocket = sockets.get(fileno)
    print str(clientSocket)
    data = 0
    #while sys.getsizeof(data) != buf:
    try:
        data = clientSocket.recv(buf)
        print data
        #echo the message back to the client
        clientSocket.send(data)
    except:
        print "socket exception"
        pass
   

if __name__ == '__main__':
    setup('localhost', 7000, 1024, 3)
