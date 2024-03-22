from config import *
import http.client
import json


def send_get_request():
    server_address = CLIENT_IP
    server_port = CLIENT_PORT

    conn = http.client.HTTPConnection(server_address, server_port)

    conn.request("GET", "/menu")

    response = conn.getresponse()

    data = response.read()

    print("Response from server:")
    print(data.decode('utf-8'))

    conn.close()

def send_post_request():
    server_address = CLIENT_IP
    server_port = CLIENT_PORT

    conn = http.client.HTTPConnection(server_address, server_port)

    pedido = {
        'productos': [
            {'producto': 'Hamburguesa', 'cantidad': 2}
        ]
    }

    pedido_json = json.dumps(pedido)
    headers = {'Content-type': 'application/json'}

    conn.request("POST", "/pedido", pedido_json, headers)

    print("Pedido enviado")
    response = conn.getresponse()

    data = response.read()

    print("Response from server:")
    print(data.decode('utf-8'))

    conn.close()


# Una vez acceda a la pagina web, debera obtener la lista de pedidos y mostrarla en la pagina web, para luego mandar a preparar los pedidos.

if __name__ == "__main__":
    send_get_request()
    send_post_request()
