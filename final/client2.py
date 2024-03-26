from config import *
from utils import send_get_request, send_post_request, get_task_status

pedido = {
    'productos': [
        {'producto': 'Pizza', 'cantidad': 2}
    ]
}


if __name__ == "__main__":
    send_get_request(CLIENT2_IP, CLIENT2_PORT)
    task_id = send_post_request(CLIENT2_IP, CLIENT2_PORT, pedido)
    get_task_status(CLIENT2_IP, CLIENT2_PORT, task_id)
