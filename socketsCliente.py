import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('', 27007))
print('conectado al servidor, escriba "chau" para cerrar su conxión')


while True:
    data=(input('Mensaje:'))
    s.sendall(data.encode('utf-8'))
    if data == 'chau':
        print('cerrando conexiòn')
        break

    servidorMsj = s.recv(1024)
    if servidorMsj != None:
        print(servidorMsj.decode("utf-8"))
    elif 'chau' in data.decode('utf-8'):
        print('cerrando conexiòn')
        break
    else:
        pass
    

s.close()