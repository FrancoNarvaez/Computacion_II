import http.client
import json
import time


def parse_arguments():
    #Manejar aca el parceo de manera generica para no repetir codigo
    pass


def send_get_request(cliente_ip, cliente_port):
    server_address = cliente_ip
    server_port = cliente_port
    conn = http.client.HTTPConnection(server_address, server_port)
    conn.request("GET", "/menu")
    response = conn.getresponse()
    data = response.read()
    print("Response from server:")
    print(data.decode('utf-8'))

    conn.close()


def send_post_request(cliente_ip, cliente_port, pedido):
    server_address = cliente_ip
    server_port = cliente_port
    conn = http.client.HTTPConnection(server_address, server_port)
    pedido_json = json.dumps(pedido)
    headers = {'Content-type': 'application/json'}
    conn.request("POST", "/pedido", pedido_json, headers)

    print("\nPedido enviado")
    response = conn.getresponse()
    data = response.read()
    print("Response from server:")
    task_id = data.decode('utf-8')
    print(task_id)

    conn.close()
    return task_id


def get_task_status(cliente_ip, cliente_port, task_id):
    server_address = cliente_ip
    server_port = cliente_port

    while True:
        try:
            conn = http.client.HTTPConnection(server_address, server_port)
            conn.request("GET", f"/status/{task_id}")
            response = conn.getresponse()
            data = response.read()
            # Decodifica la respuesta JSON
            task_data = json.loads(data.decode('utf-8'))
            print("\nResponse from server:")
            print(task_data)
            # Verifica el estado del pedido
            if task_data.get('estado') == 'Completado':

                conn.close()
                break

            conn.close()
            time.sleep(7)  # Espera 20 segundos antes de consultar de nuevo
        except http.client.RemoteDisconnected:
            print("Server disconnected. Retrying in 3 seconds...")
            time.sleep(3)
