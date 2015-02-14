from socket import *
import threading
import time
import datetime
import random

 
def handleTheSocket(clientNumber):
    host = '192.168.0.13'
    port = 7000
    buf = 2048
    #clientNumber = 5
    addr = (host, port)
 
    clientsocket = socket(AF_INET, SOCK_STREAM)
  
    clientsocket.connect(addr)
  
    while 1:
      
      data =  "hi I'm " + str(clientsocket.getsockname()) + "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vehicula ante at libero accumsan, a pretium metus molestie. Fusce sit amet feugiat neque. Praesent posuere diam vel tincidunt mattis. Curabitur eleifend turpis velit, et ornare urna ultricies eu. Fusce elementum nisi et nibh finibus, at malesuada elit vestibulum. Suspendisse vitae ante ultrices, blandit nunc eu, auctor arcu. Vestibulum consequat, nunc vel posuere varius, tortor eros pulvinar orci, vel viverra eros ante ut sem. Cras dapibus est eu lacus condimentum, at volutpat orci rutrum. Aliquam eget tellus nec est egestas fringilla. Pellentesque in tincidunt arcu. Morbi rhoncus est nibh, et facilisis elit tincidunt et. In porta ex ex, ac vehicula diam lacinia nec. Fusce convallis in turpis at pulvinar. Morbi dapibus nisl purus. Quisque ligula mauris, fringilla et purus sit amet, convallis ornare arcu.Donec vitae mi sed leo pulvinar luctus. Nulla fermentum elit at mauris varius malesuada. Quisque nibh justo, interdum ac sapien in, consectetur tempus risus. Morbi sodales velit imperdiet, sollicitudin urna at, rutrum mi. Etiam sit amet molestie quam, sit amet semper velit. Maecenas enim velit, cursus eu lacus vel, placerat elementum enim. Maecenas elementum orci et mauris imperdiet ornare. Morbi pulvinar est sed semper euismod. Phasellus dolor diam, rhoncus non nunc vitae, mattis feugiat diam. Proin volutpat dolor elit, ut cursus felis convallis non. Nullam posuere nisl ac varius fringilla.Vestibulum eu feugiat neque. Suspendisse egestas lectus nulla, eu viverra metus viverra in. Nam hendrerit diam tellus, eleifend egestas erat tempus et. Vestibulum ultrices eget justo at lobortis. Donec dolor nulla, aliquam vitae augue nec, aliquet eleifend ipsum. Donec eros orci, lacinia et posuere id, laoreet quis justo. Nunc id erat a nibh convallis feugiat. Nunc congue euismod neque, in fringilla nunc tempus non. Morbi vehicula nibh ac malesuada viverra. Vivamus maximus diam metus, id fringilla magna semper amet."
      #raw_input("Send the server a message! >>>")
      clientsocket.send(data)
      data = clientsocket.recv(buf)
      print data + '\n'
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
      