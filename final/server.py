import socket
import json
import uuid
import logging
from order import Order
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from task import app, check_ingredients, prepare
from celery import chain

logging.basicConfig(level=logging.INFO)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        logging.info(f"Cliente conectado desde la IP: {client_ip}")
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
        client_ip = self.client_address[0]
        logging.info(f"Cliente conectado desde la IP: {client_ip}")
        if self.path == '/pedido':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))

            # Genera un id_pedido
            id_pedido = str(uuid.uuid4())
            params['id_pedido'] = id_pedido

            order = Order(params)

            # Encadena las tareas
            workflow = chain(check_ingredients.s(order.order_dict), prepare.s())
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


class DualStackServer(ThreadingHTTPServer):
    def server_bind(self):
        try:
            # Configura el socket para ser reutilizable
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if self.address_family == socket.AF_INET6:
                # Si estamos utilizando IPv6, configura el socket para aceptar conexiones IPv4 también
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            ThreadingHTTPServer.server_bind(self)
        except Exception as e:
            logging.error(f"Conexión rechazada: {e}")
            raise


def start_http_server():
    server_address = ('', 8080)

    httpd = DualStackServer(server_address, RequestHandler)

    print(f'Starting HTTP server on {server_address[0]}:{server_address[1]}')
    httpd.serve_forever()


if __name__ == "__main__":
    start_http_server()
