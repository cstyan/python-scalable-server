from socket import *
import select
import thread
import getopt

#initial setup, including server socket and registration with the epoll object
def setup():
    #access all the globals
    global epoll
    global sockets
    global requests
    global responses
    global buf
    global serverSocket
    global port
    global threads
    #init
    sockets = {}
    requests = {}
    responses = {}
    #socket setup
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', port))
    serverSocket.listen(100)
    serverSocket.setblocking(0)
    #create epoll object
    epoll.select.epoll()
    epoll.register(serverSocket.fileno(), select.EPOLLIN)

    for x in range(o, threads):
        thread.start_new_thread(threadFunc, ())
        print "thread created"

    threadFunc()

#main driver for each thread
def threadFunc():
    global sockets
    global requests
    global responses
    global serverSocket
    global epoll
    print " starting infinite loop"

    try:
        while True:
            events = epoll.poll(-1)
            for fileno, event in events:
                if fileno == serverSocket.fileno()
                    connection, address = serverSocket.accept()
                    connection.setblocking(0)
                    epoll.register(connection.fileno(), select.EPOLLIN)
                    sockets[connection.fileno()] = connection
                    requests[connection.fileno()] = b''
                    responses[connection.fileno] = b''
                elif event & select.EPOLLIN:
                    requests[fileno] += sockets[fileno].recv(buf)
                    epoll.modify(fileno, select.EPOLLOUT)
                elif event & select.EPOLLOUT:
                    byteswritten = sockets[fileno].send(responses[fileno])
                    responses[fileno] = responses[fileno][byteswritten:]
                    if len(responses[fileno]) == 0
                        epoll.modify(fileno, 0)
                        sockets[fileno].shutdown(socket.SHUT_RDWR)
                    elif event & select.EPOLLHUP:
                        epoll.unregister(fileno)
                        sockets[fileno].close
                        del sockets[fileno]
        finally:
            epoll.unregister(serverSocket)
            epoll.close()
            serverSocket.close()

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