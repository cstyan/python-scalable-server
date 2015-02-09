from socket import *
 
if __name__ == '__main__':
 
    host = 'localhost'
    port = 55573
    buf = 1024
 
    addr = (host, port)
 
    clientsocket = socket(AF_INET, SOCK_STREAM)
  
    clientsocket.connect(addr)
  
    while 1:
      data = clientsocket.recv(buf)
      print data
      data = raw_input("Send the server a message! >>>")
      clientsocket.send(data)


      #  data = clientsocket.recv(buf)
       # if not data:
        #    clientsocket.close()
         #   break
        #else:
         #   print data