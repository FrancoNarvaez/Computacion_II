from config import CLIENTS
from utils import send_get_request, send_post_request, get_task_status

pedido = {
    'productos': [
        {'producto': 'Pizza', 'cantidad': 2}
    ]
}


if __name__ == "__main__":
    send_get_request(CLIENTS[1]['ip'], CLIENTS[1]['port'])
    task_id = send_post_request(CLIENTS[1]['ip'], CLIENTS[1]['port'], pedido)
    get_task_status(CLIENTS[1]['ip'], CLIENTS[1]['port'], task_id)
