import socket, os, sys, multiprocessing
import signal
from multiprocessing import Process



signal.signal(signal.SIGCHLD, signal.SIG_IGN)
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ""
port = 50006
serversocket.bind((host, port))

serversocket.listen(5)

def active():
    while True:
        try:
            msg = clientsocket.recv(1024)
            print("Recibido: %s" % msg.decode().upper())
            if msg == b"exit":
                print("cerrando conexion")
                clientsocket.close()
                break
            msg = "Ok"+" \r\n"
            clientsocket.send(msg.encode("utf-8"))
        except:
            break

try:
    while True:
        print("Esperando conexiones \n", serversocket)
        clientsocket, addr = serversocket.accept()
        print("Conexión desde %s" % str(addr))

        p = Process(target=active, args=())
        msg = 'Gracias por conectar'+ "\r\n"
        clientsocket.send(msg.encode('ascii'))
        p.start()


except KeyboardInterrupt:
    print('Interrupción manual, cerrando socket pasivo')    
    p.join()
    clientsocket.close()
    serversocket.close() #solo para caso practico
finally:
    print("cerrando pasivo y el proceso")
    p.join()
    serversocket.close()

