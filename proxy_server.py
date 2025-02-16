import logging
import socketserver
import http.server
import urllib.request
from urllib.parse import urlparse, urlunparse, quote, parse_qs
import re

logging.basicConfig(level=logging.INFO)

class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Check for query parameters or root path
        if self.path == "/" or "?" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Proxy Server Running</h1></body></html>")
            return

        url = self.path[1:]
        logging.info(f"Received GET request for URL: {url}")

        if not url.startswith(('http://', 'https://')):
            self.send_error(400, "Only absolute URLs are allowed")
            return

        try:
            with urllib.request.urlopen(url) as response:
                self.send_response(response.status)
                for header in response.getheaders():
                    self.send_header(header[0], header[1])
                self.end_headers()
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' in content_type:
                    html = response.read().decode('utf-8')
                    proxied_html = self.rewrite_urls(html, url)
                    self.wfile.write(proxied_html.encode('utf-8'))
                else:
                    self.wfile.write(response.read())
        except urllib.error.HTTPError as e:
            self.send_error(e.code, f"HTTP Error: {e.reason}")
        except urllib.error.URLError as e:
            self.send_error(404, f"URL Error: {e.reason}")
        except Exception as e:
            self.send_error(500, f"Server Error: {e}")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        url = self.path[1:]
        logging.info(f"Received POST request for URL: {url}")

        if not url.startswith(('http://', 'https://')):
            self.send_error(400, "Only absolute URLs are allowed")
            return

        try:
            req = urllib.request.Request(url, data=post_data, method='POST')
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for header in response.getheaders():
                    self.send_header(header[0], header[1])
                self.end_headers()
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' in content_type:
                    html = response.read().decode('utf-8')
                    proxied_html = self.rewrite_urls(html, url)
                    self.wfile.write(proxied_html.encode('utf-8'))
                else:
                    self.wfile.write(response.read())
        except urllib.error.HTTPError as e:
            self.send_error(e.code, f"HTTP Error: {e.reason}")
        except urllib.error.URLError as e:
            self.send_error(404, f"URL Error: {e.reason}")
        except Exception as e:
            self.send_error(500, f"Server Error: {e}")

    def rewrite_urls(self, html, base_url):
        parsed_base_url = urlparse(base_url)
        base_url_netloc = f"{parsed_base_url.scheme}://{parsed_base_url.netloc}"

        def replace_url(match):
            orig_url = match.group(0)
            new_url = urlparse(orig_url, scheme=parsed_base_url.scheme)
            if new_url.netloc == '':
                new_url = new_url._replace(netloc=parsed_base_url.netloc)
            proxied_url = f"/{quote(urlunparse(new_url))}"
            return proxied_url

        pattern = re.compile(r'(https?://[^\s\'"<>]+|href=[\'"]?([^\'" >]+))')
        proxied_html = pattern.sub(replace_url, html)
        return proxied_html

if __name__ == "__main__":
    PORT = 8888
    with socketserver.TCPServer(("", PORT), Proxy) as httpd:
        logging.info(f"Serving on port {PORT}")
        httpd.serve_forever()
