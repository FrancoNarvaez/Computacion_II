from config import *
from utils import send_get_request, send_post_request, get_task_status


pedido = {
    'productos': [
        {
         'producto': 'Hamburguesa',
         'cantidad': 2
        },
        {
         'producto': 'Pizza',
         'cantidad': 2
        },
        {
         'producto': 'Ensalada',
         'cantidad': 2
        }
    ]
}

if __name__ == "__main__":
    send_get_request(CLIENT_IP, CLIENT_PORT)
    task_id = send_post_request(CLIENT_IP, CLIENT_PORT, pedido)
    get_task_status(CLIENT_IP, CLIENT_PORT, task_id)
