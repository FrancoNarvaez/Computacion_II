from config import *
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/menu':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Menu del restaurante:\n- Pizza\n- Hamburguesa\n- Ensalada")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Error 404: Not Found")

    def do_POST(self):
        if self.path == '/pedido':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))

            # Procesa el pedido
            for producto_dict in params['productos']:
                producto = producto_dict['producto']
                cantidad = producto_dict['cantidad']
            # Aquí aplicar la lógica para procesar el pedido, como si existe, si quedan ingredientes, etc.

            # Responder al cliente con el estado del pedido
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Pedido recibido y en proceso")
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

