import socket
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


class MyHandler(SimpleHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == "/health-check":
            self._set_headers()
            return
        elif self.path == "/":
            self._set_headers()
            self.wfile.write("chronos is timeless, server {}".format(get_ip()))
            return
        else:
            self.send_error(404)
            return

    def do_HEAD(self):
        self._set_headers()


if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 3001), MyHandler)
    server.serve_forever()
