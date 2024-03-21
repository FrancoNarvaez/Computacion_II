from config import *
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler


class ServerHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # En wfile mandar la pagina principal de la aplicacion web
        self.wfile.write(b"URL de la pagina web")


def start_http_server():
    server_address = (SERVER_IP, SERVER_PORT)

    httpd = ThreadingHTTPServer(server_address, ServerHTTPRequestHandler)

    print(f'Starting HTTP server on {SERVER_IP}:{SERVER_PORT}')
    httpd.serve_forever()


if __name__ == "__main__":
    start_http_server()

