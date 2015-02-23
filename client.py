# Source File: client.py - simple multithreaded echo client
# Program: Scalable Server Methods 8005A2
# Functions:
#     setup
#     handler
#     main
# Date: February 23, 2015
# Designer: Callum Styan, Jon Eustace
# Programmer: Callum Styan, Jon Eustace
from socket import *
import datetime
import threading
import time
import datetime
import random
import sys
import getopt

global serverIP
global port
global buf #buffer size
global msg #num of msgs to send
global clients
global msgStr
global times
global fileName
msgStr = ""
times = {}

# Function: genMsg
# Interface: genMsg()
#
# Designer: Callum Styan
# Programmer: Callum Styan
#
# Description: This function generates a
# message of the specified length for the
# client to send.
def genMsg():
    global msgStr
    i = 0
    while i < buf:
        msgStr += 'a'
        i += 1

# Function: genMsg
# Interface: genMsg()
#
# Designer: Callum Styan, Jon Eustace
# Programmer: Callum Styan, Jon Eustace
#
# Description: This function handles sending
# and receiving data on the client.  It also
# keeps track of RTT's for logging after all
# messages have been sent. 
def handleTheSocket(clientNumber):
    global times
    global serverIP
    addr = (serverIP, port) 
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientsocket.connect(addr)

    i = 0
    start = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    while i < msg:
        clientsocket.send(msgStr)
        data = clientsocket.recv(buf)
        i += 1

    end = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    duration = int(end) - int(start)
    times.update({threading.current_thread():duration})

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
    global serverIP
    global port
    global buf
    global msg
    global clients
    global fileName

    print " getting arguments"

    try:
        opts, args = getopt.getopt(argv, "s:p:b:n:c:o:h",["serverIP=","port=","bufferSize=", "numMsg=" "numClients=", "output=", "help"])
    except getopt.GetoptError:
        print 'client.py -s <serverIP> -p <port> -b <bufferSize> -n <numMsg> -c <numClients> -o <output>'
        sys.exit(2)
    
    if len(sys.argv) < 6:
        print 'client.py -s <serverIP> -p <port> -b <bufferSize> -n <numMsg> -c <numClients> -o <output>'
        sys.exit()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'client.py -s <serverIP> -p <port> -b <bufferSize> -n <numMsg> -c <numClients> -o <output>'
            sys.exit()
            port = int(arg)
        elif opt in ("-s", "--serverIP"):
            serverIP = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-b", "--bufferSize"):
            buf = int(arg)
        elif opt in ("-n", "--numMsg"):
            msg = int(arg)
        elif opt in ("-c", "--numClients"):
            clients = int(arg)
        elif opt in("-o", "--output"):
            fileName = arg

#main method of the program
if __name__ == '__main__':
    main(sys.argv[1:])
    threads = []

    print "serverIP: %s" % serverIP
    print "port: %d" % port
    print "buffer: %d" % buf
    print "numMsgs: %d" % msg
    print "numClients: %d" % clients
    #print "buffer: %d" % buf
    genMsg()

    for x in range(clients):
        thread = threading.Thread(target = handleTheSocket, args = [x])
        thread.start()
        threads.append(thread)
       
    for thread in threads:
        thread.join()
    
    print "threads are finished"
    with open(fileName, 'w') as f:  
        for key in times:
            avg = times[key] / msg
            ms = float(avg) / 1000
            f.write(str(ms) + "\n")

    print "done"