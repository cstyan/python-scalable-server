from socket import *
import select
import thread
import sys
import getopt

# buf = 2048
# sockets = {}
# epoll = select.epoll()
# threads = 3
# port = 7000

#initial setup, including server socket and registration with the epoll object
def setup():
    #access all the globals
    global epoll
    global sockets
    global buf
    global serverSocket
    global port
    global threads
    global dataSent
    global dataRecvd

    #init
    epoll = select.epoll()
    sockets = {}
    dataSent = 0
    dataRecvd = 0

    print "threads: %d" % threads
    print "port: %d" % port
    print "buffer: %d" % buf

    #socket setup
    serverSocket = socket(AF_INET, SOCK_STREAM)
    #serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    epoll.register(serverSocket, select.EPOLLIN | select.EPOLLET)
    #add the server socket to the global sockets collection
    sockets.update({serverSocket.fileno(): serverSocket})
    #should this be before or after
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', port))
    serverSocket.listen(1)
    serverSocket.setblocking(0)

    #start the threads, they all have access to the global epoll object and all sockets
    for x in range(0, threads):
        thread.start_new_thread(threadFunc, ())
        print "thread created"

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
    global epoll
    global dataSent
    global dataRecvd

    clientSocket = sockets.get(fileno)
    print "receiving data from socket"
    data = clientSocket.recv(buf)
    dataRecvd += len(data)
    print dataRecvd
    print len(data)
    print "all data sent, echoing back to client"
    #echo back to client
    if(data != ""):
        clientSocket.sendall(data)
        dataSent += len(data)
        print dataSent
        print "data echoed to client"

    # clientSocket = sockets.get(fileno)
    # data = 0
    # #while sys.getsizeof(data) != buf:
    # echoed = False
    # while echoed == False:
    #     data = ''
    #     while len(data) < buf:
    #         try:
    #             data = clientSocket.recv(buf - len(data))
    #         except:
    #             print "Socket exception, removing that client."
    #             print "Exception was: ", sys.exc_info()
    #             #del sockets[fileno]
    #             #epoll.unregister(fileno)
    #             pass
    #     #end of while loop
    #     while data:
    #         sent = sock.send(data)
    #         data = data[sent:]

    #     echoed = True
   

def main(argv):
    global threads
    global port
    global buf

    try:
        opts, args = getopt.getopt(argv, "t:p:b:h",["threads=","port=","buffer=", "help"])
    except getopt.GetoptError:
        #print 'edgeTriggered.py -t <numThreads> -p <port> -b <bufferSize>'
        usage()
        sys.exit(2)
    
    if len(sys.argv) < 3:
        print 'edgeTriggered.py -t <numThreads> -p <port> -b <bufferSize>'
        sys.exit()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'edgeTriggered.py -t <numThreads> -p <port> -b <bufferSize>'
            sys.exit()
        elif opt in ("-t","--threads"):
            threads = int(arg)
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-b", "--buffer"):
            buf = int(arg)


if __name__ == '__main__':
    main(sys.argv[1:])
    setup()
