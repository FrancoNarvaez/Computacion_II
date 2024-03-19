import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('0.0.0.0', 27007))

s.settimeout(35)

s.listen(2)
print('escuchando')

try:
    conn, addr = s.accept()
    print("Conexión aceptada de:", addr)

    while True:    
        conn.settimeout(30)
    
        data = conn.recv(1024)
        print(data.decode("utf-8"))

        if 'chau' in data.decode('utf-8'):
            conn.close()
            break

        mensaje1 = (input('Mensaje:'))
        respuesta = conn.sendall(mensaje1.encode("utf-8"))

except KeyboardInterrupt:
  print('Interrupción manual, cerrando socket pasivo')

finally:
  print('cerrando servidor pasivo')
  s.close()
