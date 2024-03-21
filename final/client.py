from config import *
import http.client


def send_get_request():
    server_address = CLIENT_IP
    server_port = CLIENT_PORT

    conn = http.client.HTTPConnection(server_address, server_port)

    conn.request("GET", "/")

    response = conn.getresponse()

    data = response.read()

    print("Response from server:")
    print(data.decode('utf-8'))

    conn.close()

# Una vez acceda a la pagina web, debera obtener la lista de pedidos y mostrarla en la pagina web, para luego mandar a preparar los pedidos.

if __name__ == "__main__":
    send_get_request()
