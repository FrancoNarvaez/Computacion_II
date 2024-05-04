import threading
from utils import send_get_request, send_post_request, get_task_status
from config import CLIENTS


pedido1 = {
    'productos': [
        {
            'producto': 'Hamburguesa',
            'cantidad': 2
        },
        {
            'producto': 'Pizza',
            'cantidad': 1
        },
        {
            'producto': 'Ensalada',
            'cantidad': 3
        }
    ]
}
pedido2 = {
    'productos': [
        {
            'producto': 'Pizza',
            'cantidad': 2
        },
        {
            'producto': 'Refresco',
            'cantidad': 1
        },
        {
            'producto': 'Agua',
            'cantidad': 1
        }
    ]
}
pedido3 = {
    'productos': [
        {
            'producto': 'Milanesa',
            'cantidad': 2
        },
        {
            'producto': 'Papas fritas',
            'cantidad': 1
        },
        {
            'producto': 'Hot dog',
            'cantidad': 1
        }
    ]
}
pedido4 = {
    'productos': [
        {
            'producto': 'Tacos',
            'cantidad': 2
        },
        {
            'producto': 'Hamburguesa',
            'cantidad': 1
        },
        {
            'producto': 'Pizza',
            'cantidad': 1
        }
    ]
}


def handle_client(client, pedido):
    send_get_request(client['ip'], client['port'])
    task_id = send_post_request(client['ip'], client['port'], pedido)
    get_task_status(client['ip'], client['port'], task_id)


def start_threads():
    threads = []
    for i in range(len(CLIENTS)):
        t = threading.Thread(target=handle_client, args=(CLIENTS[i], pedidos[i]))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    pedidos = [pedido1, pedido2]  # pedido3, pedido4]

    print(len(CLIENTS))
    if len(CLIENTS) > len(pedidos):
        print("Menos pedidos que clientes")

    if len(pedidos) > len(CLIENTS):
        print("Mas pedidos que clientes")

    start_threads()
