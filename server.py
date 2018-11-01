#!/usr/bin/env python
import urllib2
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


class MyHandler(SimpleHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == "/health-check":
            self._set_headers()
        elif self.path == "/":
            self._set_headers()
            self.wfile.write("chronos is timeless")
        else:
            self.send_error(404)

    def do_HEAD(self):
        self._set_headers()


if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 3001), MyHandler)
    server.serve_forever()