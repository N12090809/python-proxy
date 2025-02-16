import logging
import socketserver
import http.server
import urllib.request
from urllib.parse import urlparse, urlunparse, quote
import re

logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG for detailed logs

class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        logging.debug(f"Handling GET request: Path = {self.path}")

        url = self.path[1:]
        logging.info(f"Received GET request for URL: {url}")

        if not url:
            logging.debug("Empty URL, returning proxy server message")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Proxy Server Running</h1></body></html>")
            return

        if url == "favicon.ico":
            logging.debug("Request for favicon.ico, returning 204 No Content")
            self.send_response(204)  # No Content
            self.end_headers()
            return

        if not url.startswith(('http://', 'https://')):
            logging.warning("Invalid URL: Only absolute URLs are allowed")
            self.send_error(400, "Only absolute URLs are allowed")
            return

        try:
            logging.info(f"Fetching URL: {url}")
            with urllib.request.urlopen(url) as response:
                logging.debug(f"Response received for URL: {url}")
                self.send_response(response.status)
                for header in response.getheaders():
                    self.send_header(header[0], header[1])
                self.end_headers()
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' in content_type:
                    logging.debug(f"Processing HTML content from URL: {url}")
                    html = response.read().decode('utf-8')
                    proxied_html = self.rewrite_urls(html, url)
                    self.wfile.write(proxied_html.encode('utf-8'))
                else:
                    logging.debug(f"Processing non-HTML content from URL: {url}")
                    self.wfile.write(response.read())
        except urllib.error.HTTPError as e:
            logging.error(f"HTTP Error: {e.code}, Reason: {e.reason}")
            self.send_error(e.code, f"HTTP Error: {e.reason}")
        except urllib.error.URLError as e:
            logging.error(f"URL Error: {e.reason}")
            self.send_error(404, f"URL Error: {e.reason}")
        except Exception as e:
            logging.error(f"Server Error: {e}")
            self.send_error(500, f"Server Error: {e}")

    def do_POST(self):
        logging.debug(f"Handling POST request: Path = {self.path}")

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        url = self.path[1:]
        logging.info(f"Received POST request for URL: {url}")

        if not url or not url.startswith(('http://', 'https://')):
            logging.warning("Invalid URL: Only absolute URLs are allowed")
            self.send_error(400, "Only absolute URLs are allowed")
            return

        try:
            logging.info(f"Fetching URL: {url}")
            req = urllib.request.Request(url, data=post_data, method='POST')
            with urllib.request.urlopen(req) as response:
                logging.debug(f"Response received for URL: {url}")
                self.send_response(response.status)
                for header in response.getheaders():
                    self.send_header(header[0], header[1])
                self.end_headers()
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' in content_type:
                    logging.debug(f"Processing HTML content from URL: {url}")
                    html = response.read().decode('utf-8')
                    proxied_html = self.rewrite_urls(html, url)
                    self.wfile.write(proxied_html.encode('utf-8'))
                else:
                    logging.debug(f"Processing non-HTML content from URL: {url}")
                    self.wfile.write(response.read())
        except urllib.error.HTTPError as e:
            logging.error(f"HTTP Error: {e.code}, Reason: {e.reason}")
            self.send_error(e.code, f"HTTP Error: {e.reason}")
        except urllib.error.URLError as e:
            logging.error(f"URL Error: {e.reason}")
            self.send_error(404, f"URL Error: {e.reason}")
        except Exception as e:
            logging.error(f"Server Error: {e}")
            self.send_error(500, f"Server Error: {e}")

    def rewrite_urls(self, html, base_url):
        logging.debug(f"Rewriting URLs in the HTML content")
        parsed_base_url = urlparse(base_url)
        base_url_netloc = f"{parsed_base_url.scheme}://{parsed_base_url.netloc}"

        def replace_url(match):
            orig_url = match.group(0)
            logging.debug(f"Original URL: {orig_url}")
            new_url = urlparse(orig_url, scheme=parsed_base_url.scheme)
            if new_url.netloc == '':
                new_url = new_url._replace(netloc=parsed_base_url.netloc)
            proxied_url = f"/{quote(urlunparse(new_url))}"
            logging.debug(f"Proxied URL: {proxied_url}")
            return proxied_url

        pattern = re.compile(r'(https?://[^\s\'"<>]+|href=[\'"]?([^\'" >]+))')
        proxied_html = pattern.sub(replace_url, html)
        logging.debug(f"URLs rewritten in the HTML content")
        return proxied_html

if __name__ == "__main__":
    PORT = 8888
    with socketserver.TCPServer(("", PORT), Proxy) as httpd:
        logging.info(f"Serving on port {PORT}")
        httpd.serve_forever()
