from socket import *
 
if __name__ == '__main__':
 
    host = 'localhost'
    port = 55568
    buf = 1024
 
    addr = (host, port)
 
    clientsocket = socket(AF_INET, SOCK_STREAM)
  
   //test
    clientsocket.connect(addr)
    data = raw_input(">> ")
    while 1:
      
        if not data:
            break
        else:
            clientsocket.send(data)
            data = clientsocket.recv(buf)
            if not data:
                break
            else:
                print data
    clientsocket.close()