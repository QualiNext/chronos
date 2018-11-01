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
            req = urllib2.Request('http://localhost:3001')
            response = urllib2.urlopen(req)
            content = response.read()
            self.wfile.write(content)
        else:
            self.send_error(404)

    def do_HEAD(self):
        self._set_headers()


if __name__ == '__main__':
    client = HTTPServer(('127.0.0.1', 3000), MyHandler)
    client.serve_forever()