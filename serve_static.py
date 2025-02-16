import http.server
import socketserver
import os

PORT = 8000

class StaticHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="static", **kwargs)

with socketserver.TCPServer(("", PORT), StaticHandler) as httpd:
    print(f"Serving static files on port {PORT}")
    httpd.serve_forever()

