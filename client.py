from socket import *
import threading
import time
import datetime
import random

 
def handleTheSocket(clientNumber):
    host = '192.168.0.13'
    port = 7000
    buf = 1024
    #clientNumber = 5
    addr = (host, port)
 
    clientsocket = socket(AF_INET, SOCK_STREAM)
  
    clientsocket.connect(addr)
  
    while 1:
      data = clientsocket.recv(buf)
      print data + '\n'
      data =  "hi I'm " + str(clientsocket.getsockname())
      #raw_input("Send the server a message! >>>")
      clientsocket.send(data)
      t = random.randint(0, 0)
      time.sleep(t)

if __name__ == '__main__':
 
        threads = []

        for x in range(10000):
            thread = threading.Thread(target = handleTheSocket, args = [x])
            thread.start()
            threads.append(thread)
           

        for thread in threads:
            thread.join()
      