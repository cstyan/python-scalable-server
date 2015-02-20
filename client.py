from socket import *
import threading
import time
import datetime
import random

 
def handleTheSocket(clientNumber):
    host = 'localhost'
    port = 8005
    buf = 2048
    #clientNumber = 5
    addr = (host, port)
 
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientsocket.connect(addr)
  
    while 1:
      
      data =  "hi I'm " + str(clientsocket.getsockname()) +"373248644238091033361171340508505162629570915145962037766433373137770359367676167852752348371395682890859173122892676240122689740006895490189156549494689538759749967414623425907742325632425691232808842595508894358621128519780747236911707915627432006418367432030047000243176184421517923026449506670356"
      #raw_input("Send the server a message! >>>")
      clientsocket.send(data)
      print "sent data"
      data = clientsocket.recv(buf)
      print data + '\n'
      t = random.randint(0, 0)
      time.sleep(t)

if __name__ == '__main__':
 
        threads = []

        for x in range(10):
            thread = threading.Thread(target = handleTheSocket, args = [x])
            thread.start()
            threads.append(thread)
           

        for thread in threads:
            thread.join()
      
