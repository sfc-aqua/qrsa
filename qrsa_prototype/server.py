from http.server import HTTPServer, BaseHTTPRequestHandler
import socket


hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # ターミナルにリクエストを表示
        print(f"got request: {self.path}")

        # レスポンスを送信
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, World! ' + str(ip_address).encode("ascii") )
    


def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    print("hello ", f"{ip_address}:{8080}")
    httpd.serve_forever()

run()