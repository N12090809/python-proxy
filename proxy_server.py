import socketserver
import http.server
import urllib.request
from urllib.parse import urlparse, urlunparse, quote
import re

class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = self.path[1:]
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
        except Exception as e:
            self.send_error(404, f"Error: {e}")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        url = self.path[1:]
        try:
            req = urllib.request.Request(url, data=post_data, method='POST')
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for header in response.getheaders():
                    self.send_header(header[0], header[1])
                self.end_headers()
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' in content type:
                    html = response.read().decode('utf-8')
                    proxied_html = self.rewrite_urls(html, url)
                    self.wfile.write(proxied_html.encode('utf-8'))
                else:
                    self.wfile.write(response.read())
        except Exception as e:
            self.send_error(404, f"Error: {e}")

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
        print(f"Serving on port {PORT}")
        httpd.serve_forever()
