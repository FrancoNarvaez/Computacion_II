import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


host = ""
port = 50006

print("Haciendo el connect")
s.connect((host, port))   
print("Handshake realizado con exito!")

while True:
    data=(input('Mensaje:'))
    s.sendall(data.encode('utf-8'))
    if data == 'exit':
        print('cerrando conexiòn')
        break

    msg = s.recv(1024)                                     
    if msg != None:
        print(msg.decode("utf-8"))
    elif 'exit' in data.decode('utf-8'):
        print('cerrando conexiòn')
        s.close()
        break
    else:
        print("Cerrando conexion")
        s.close()
     