import http.server
import socketserver
import socket
import json

HOST = 'localhost'
PORT = 3000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        message_data = json.loads(post_data)

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            client_socket.sendto(post_data.encode('utf-8'), (HOST, 5000))

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

def main():
    socket_server = socketserver.ThreadingTCPServer(('localhost', PORT), MyHttpRequestHandler)
    print(f'HTTP server is running on {HOST}:{PORT}')
    socket_server.serve_forever()

if __name__ == '__main__':
    main()
