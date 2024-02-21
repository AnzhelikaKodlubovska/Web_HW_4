from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import json
from datetime import datetime
import socket

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        message_data = json.loads(post_data)

        self.save_to_json(message_data)

        self.send_response(302)
        self.send_header('Location', '/message')
        self.end_headers()

    def save_to_json(self, data):
        with open('storage/data.json', 'a') as file:
            json.dump(data, file, indent=2)
            file.write('\n')

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())
            
    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

def start_udp_server():
    HOST = 'localhost'
    PORT = 5000

    def save_to_json(data):
        with open('storage/data.json', 'a') as file:
            json.dump(data, file, indent=2)
            file.write('\n')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print(f'Socket server is running on {HOST}:{PORT}')

        while True:
            data, addr = server_socket.recvfrom(1024)
            data = data.decode('utf-8')
            message = json.loads(data)
            message['timestamp'] = str(datetime.now())
            save_to_json(message)
            print(f"Received message from {addr}: {message}")

if __name__ == '__main__':
    import multiprocessing
    http_server_process = multiprocessing.Process(target=run)
    udp_server_process = multiprocessing.Process(target=start_udp_server)

    http_server_process.start()
    udp_server_process.start()

    http_server_process.join()
    udp_server_process.join()
