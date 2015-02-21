from socket import *
import select
import thread
import sys
import getopt
from socket import error as SocketError
import errno

#initial setup, including server socket and registration with the epoll object
def setup():
    #create all the globals
    global epoll
    global sockets
    global buf
    global serverSocket
    global port
    global listenAmt
    global dataSent
    global dataRecvd

    #init
    epoll = select.epoll()
    sockets = {}
    dataSent = 0
    dataRecvd = 0

    print "listen amount: %d" % listenAmt
    print "port: %d" % port
    print "buffer: %d" % buf

    #socket setup
    serverSocket = socket(AF_INET, SOCK_STREAM)
    epoll.register(serverSocket, select.EPOLLIN)
    #add the server socket to the global sockets collection
    sockets.update({serverSocket.fileno(): serverSocket})
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', port))
    serverSocket.listen(listenAmt)
    serverSocket.setblocking(0)

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
    while 1:
        try:
            clientSocket, clientAddr = serverSocket.accept()
            #set non-blocking mode
            clientSocket.setblocking(0)
            #add the new client socket to the global collection
            sockets.update({clientSocket.fileno(): clientSocket})
            epoll.register(clientSocket, select.EPOLLIN | select.EPOLLET)
            #print "client connected!"
        except:
            break

#handle the incomming data event
def dataHandler(fileno):
    #access globals
    global sockets
    global buf
    global epoll
    global dataSent
    global dataRecvd

    clientSocket = sockets.get(fileno)
    try:
        data = clientSocket.recv(buf)
        dataRecvd += len(data)
        #echo back to client
        if(data != ""):
            clientSocket.sendall(data)
            dataSent += len(data)
    except SocketError as e:
        print "A socket error occurred."
        if e.errno != errno.ECONNRESET:
            raise
        pass
    #print "all data sent, echoing back to client"
   

def main(argv):
    global port
    global buf
    global listenAmt

    try:
        opts, args = getopt.getopt(argv, "l:p:b:h",["listenAmt=","port=","buffer=", "help"])
    except getopt.GetoptError:
        #usage()
        sys.exit(2)
    
    if len(sys.argv) < 3:
        print 'edgeTriggered.py -l <listenAmt> -p <port> -b <bufferSize>'
        sys.exit()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'edgeTriggered.py -l <listenAmt> -p <port> -b <bufferSize>'
            sys.exit()
            port = int(arg)
        elif opt in ("-l", "--listenAmt"):
            listenAmt = int(arg)
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-b", "--buffer"):
            buf = int(arg)


if __name__ == '__main__':
    main(sys.argv[1:])
    setup()
