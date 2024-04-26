from order import Order
from config import *
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
from configRedis import app
import uuid
from celery import chain
from prepare import prepare_ensalada, prepare_hamburguesa, prepare_pizza, prepare_refresco, prepare_agua, prepare_milanesa, prepare_papas_fritas, prepare_hot_dog, prepare_tacos

# Mapea los nombres de los productos a las funciones de preparación
product_to_function = {
    'Ensalada': prepare_ensalada,
    'Hamburguesa': prepare_hamburguesa,
    'Pizza': prepare_pizza,
    'Refresco': prepare_refresco,
    'Agua': prepare_agua,
    'Milanesa': prepare_milanesa,
    'Papas fritas': prepare_papas_fritas,
    'Hot dog': prepare_hot_dog,
    'Tacos': prepare_tacos
}


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/menu') or self.path == '/':
            menu = {
                'productos': [
                    {
                        'nombre': 'Hamburguesa',
                        'precio': 5
                    },
                    {
                        'nombre': 'Pizza',
                        'precio': 4
                    },
                    {
                        'nombre': 'Ensalada',
                        'precio': 2
                    },
                    {
                        'nombre': 'Refresco',
                        'precio': 1
                    },
                    {
                        'nombre': 'Agua',
                        'precio': 1
                    },
                    {
                        'nombre': 'Milanesa',
                        'precio': 5
                    },
                    {
                        'nombre': 'Papas fritas',
                        'precio': 2
                    },
                    {
                        'nombre': 'Hot dog',
                        'precio': 3
                    },
                    {
                        'nombre': 'Tacos',
                        'precio': 5
                    }
                ]
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(menu).encode())

        elif self.path.startswith('/status/'):
            # Extrae el id de la tarea de la URL
            task_id = self.path.strip('/status/')

            # Obtiene el resultado de la tarea
            result = app.AsyncResult(task_id)

            if result.ready():
                # Si la tarea está lista, obtén el resultado
                task_result = result.result

                # Envía el resultado al cliente
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(task_result).encode())

            else:
                # Si la tarea no está lista, envía el estado de la tarea al cliente
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": result.state}).encode())

    def do_POST(self):
        if self.path == '/pedido':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))


            # Genera un id_pedido
            id_pedido = str(uuid.uuid4())
            params['id_pedido'] = id_pedido

            # Procesa el pedido
            for producto_dict in params['productos']:
                producto = producto_dict['producto']
                cantidad = producto_dict['cantidad']

            order = Order(params)

            # Encadena las tareas
            workflow = chain(order.check_ingredients.s(self), order.prepare.s(product_to_function))
            result = workflow.delay()


            # Devuelve inmediatamente una respuesta al cliente con el id de la tarea
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(result.id.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Error 404: Not Found")


def start_http_server():
    server_address = (SERVER_IP, SERVER_PORT)

    httpd = ThreadingHTTPServer(server_address, RequestHandler)

    print(f'Starting HTTP server on {SERVER_IP}:{SERVER_PORT}\n')
    httpd.serve_forever()


if __name__ == "__main__":
    start_http_server()
