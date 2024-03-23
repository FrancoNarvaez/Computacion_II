from config import *
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
from cocina import prepare_order, check_ingredients, app
import uuid
from celery import chain



class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/status/'):
            # Extrae el id de la tarea de la URL
            task_id = self.path.strip('/status/')

            # Obtiene el resultado de la tarea
            result = app.AsyncResult(task_id)

            # Si la tarea se ha completado, obtén el resultado
            if result.ready():
                response_message = result.get().encode()
            else:
                response_message = b"En proceso"

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response_message)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Error 404: Not Found")

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

            # Encadena las tareas
            workflow = chain(check_ingredients.s(params), prepare_order.s())
            # Ejecuta la cadena de tareas
            result = workflow.apply_async()

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

    print(f'Starting HTTP server on {SERVER_IP}:{SERVER_PORT}')
    httpd.serve_forever()


if __name__ == "__main__":
    start_http_server()