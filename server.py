from socket import *
import select
import thread
import sys
import getopt
from socket import error as SocketError
import errno
 
def setup():
    global sockets
    global buf
    global serverSocket
    global port
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

    print "listenAmt: %d" % listenAmt
    print "port: %d" % port
    print "buffer: %d" % buf    

def handler(clientsocket, clientaddr):
    print info
    clientsocket.send(str(info))
    while 1:
       
        data = clientsocket.recv(1024)
        print data
        clientsocket.send(msg)        

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
 
if __name__ == "__main__":
    main(sys.argv[1:])
    setup()
    while 1:
        print "Server is listening for connections\n"
        clientsocket, clientaddr = serverSocket.accept()
        thread.start_new_thread(handler, (clientsocket, clientaddr))
    serverSocket.close()