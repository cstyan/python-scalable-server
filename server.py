# Source File: server.py - simple multithreaded echo server
# Program: Scalable Server Methods 8005A2
# Functions:
#     setup
#     handler
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
    global sockets
    global buf
    global serverSocket
    global port
    global dataSent
    global dataRecvd
    global listenAmt
    global connectionCount
    global logger 
    #init
    logger = logging.basicConfig(filename='server.log', filemode='w', format='%(asctime)s: %(message)s', level=logging.DEBUG)
    sockets = {}
    epollCollection = {}
    connectionCount = 0
    dataSent = 0
    dataRecvd = 0

    #socket setup
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', port))
    serverSocket.listen(listenAmt)

    print "listenAmt: %d" % listenAmt
    print "port: %d" % port
    print "buffer: %d" % buf    

# Function: handler
# Interface: handler(clientsocket, clientaddr)
#   clientsocket: the socket returned from the accepted
#   clientaddr: address of the client
#
# Designer: Jon Eustace
# Programmer: Jon Eustace
#
# Description: This function handles all incomming data sent
# to the server in one of the child threads.  It reads data 
# and then echoes it back to the server.
def handler(clientsocket, clientaddr):
    global dataSent
    global dataRecvd
    while 1:
        data = clientsocket.recv(buf)
        dataRecvd += len(data)
        clientsocket.send(data)
        dataSent += len(data)

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
        print 'server.py -l <listenAmt> -p <port> -b <bufferSize>'
        sys.exit()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'server.py -l <listenAmt> -p <port> -b <bufferSize>'
            sys.exit()
            port = int(arg)
        elif opt in ("-l", "--listenAmt"):
            listenAmt = int(arg)
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-b", "--buffer"):
            buf = int(arg)

#main method of the program
if __name__ == "__main__":
    main(sys.argv[1:])
    setup()
    global connectionCount
    try:
        while 1:
            clientsocket, clientaddr = serverSocket.accept()
            thread.start_new_thread(handler, (clientsocket, clientaddr))
            connectionCount += 1
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Total clients connected during test: %s" % connectionCount)
        logging.info("Total data received: %s" % dataRecvd)
        logging.info("Total data sent: %s" % dataSent)
        serverSocket.close()