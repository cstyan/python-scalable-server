# Source File: edgeTriggered.py - simple epoll ET echo server
# Program: Scalable Server Methods 8005A2
# Functions:
#     setup
#     threadFunc
#     acceptHandler
#     dataHandler
#     main
# Date: February 23, 2015
# Designer: Callum Styan, Jon Eustace
# Programmer: Callum Styan, Jon Eustace
from socket import *
import select
import thread
import sys
import getopt
from socket import error as SocketError
import errno
import logging

# Function: setup
# Interface: setup()
#
# Designer: Callum Styan, Jon Eustace
# Programmer: Callum Styan, Jon Eustace
#
# Description: This function handles all initial setup required
# for the server, including server socket and collections needed
# to keep track of the connected sockets. 
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
    global logger
    global connectionCount

    #init
    epoll = select.epoll()
    sockets = {}
    logger = logging.basicConfig(filename='levelServer.log', filemode='w', format='%(asctime)s: %(message)s', level=logging.DEBUG)
    dataSent = 0
    dataRecvd = 0
    connectionCount = 0

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

# Function: threadFunc
# Interface: threadFunc()
#
# Designer: Callum Styan, Jon Eustace
# Programmer: Callum Styan, Jon Eustace
#
# Description: This function starts the infinite loop
# that the server uses to block on epoll.  It calls
# acceptHandler or dataHandler depending on which socket
# was returned from the epoll wait function. 
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

# Function: acceptHandler
# Interface: acceptHandler()
#
# Designer: Callum Styan, Jon Eustace
# Programmer: Callum Styan, Jon Eustace
#
# Description: This function handles all accepting of
# incomming connections.  It adds the new socket to the
# correct collections and registers it with epoll. 
def acceptHandler():
    #access globals
    global sockets
    global serverSocket
    global connectionCount
    while 1:
        try:
            clientSocket, clientAddr = serverSocket.accept()
            connectionCount += 1
            #set non-blocking mode
            clientSocket.setblocking(0)
            #add the new client socket to the global collection
            sockets.update({clientSocket.fileno(): clientSocket})
            epoll.register(clientSocket, select.EPOLLIN | select.EPOLLET)
            #print "client connected!"
        except:
            break

# Function: dataHandler
# Interface: dataHandler()
#
# Designer: Callum Styan, Jon Eustace
# Programmer: Callum Styan, Jon Eustace
#
# Description: This function handles all incomming data
# events on connected sockets.  It adds the new socket
# to the correct collections and registers it with epoll.
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
   
# Function: main
# Interface: main(argv)
#   argv: command line arguments after the filename
#
# Designer: Callum Styan
# Programmer: Callum Styan
#
# Description: This function handles all command line
# arguments necessary for the program.
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
    try:
        setup()
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Total clients connected during test: %s" % connectionCount)
        logging.info("Total data received: %s" % dataRecvd)
        logging.info("Total data sent: %s" % dataSent)
        serverSocket.close()