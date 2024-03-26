from config import *
import http.client
import json
import time


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
    task_id = data.decode('utf-8')
    print(task_id)

    conn.close()

    return task_id


def get_task_status(task_id):
    server_address = CLIENT_IP
    server_port = CLIENT_PORT

    while True:
        try:
            conn = http.client.HTTPConnection(server_address, server_port)

            conn.request("GET", f"/status/{task_id}")

            response = conn.getresponse()

            data = response.read()

            print("\nResponse from server:")
            print(data.decode('utf-8'))
            if data.decode('utf-8') == "Completado":
                conn.close()
                break
            conn.close()
            time.sleep(3)  # Espera 3 segundos antes de consultar de nuevo
        except http.client.RemoteDisconnected:
            print("Server disconnected. Retrying in 5 seconds...")
            time.sleep(3)


if __name__ == "__main__":
    send_get_request()
    task_id = send_post_request()
    get_task_status(task_id)


