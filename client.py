import socket
import sys

import urllib2
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


def HandlrFactory(server_address):
    class Handlr(SimpleHTTPRequestHandler):
        def __init__(self, request, client_address, server):
            self.server_address = server_address
            SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_GET(self):
            if self.path == "/":
                self._set_headers()
                self.wfile.write("chronos is timeless, client {}".format(get_ip()))
                return
            if self.path == "/health-check":
                self._set_headers()
                return
            elif self.path == "/remote":
                self._set_headers()
                req = urllib2.Request('http://{}:3001'.format(self.server_address))
                response = urllib2.urlopen(req)
                content = response.read()
                self.wfile.write(content)
                return
            else:
                self.send_error(404)
                return

        def do_HEAD(self):
            self._set_headers()

    return Handlr


if __name__ == '__main__':
    client = HTTPServer(('127.0.0.1', 3000), HandlrFactory(sys.argv[1]))
    client.serve_forever()
