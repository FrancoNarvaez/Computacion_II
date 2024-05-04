from utils import send_get_request, send_post_request, get_task_status
from config import CLIENTS

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
    send_get_request(CLIENTS[0]['ip'], CLIENTS[0]['port'])
    task_id = send_post_request(CLIENTS[0]['ip'], CLIENTS[0]['port'], pedido)
    get_task_status(CLIENTS[0]['ip'], CLIENTS[0]['port'], task_id)
