import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


def response(path):
    if path == "/health":
        return 200, {"status": "ok"}
    if path == "/":
        return 200, {"service": "talented-week5", "version": "1.0.0"}
    return 404, {"error": "not found"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, payload = response(self.path)
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", int(os.getenv("PORT", "8080"))), Handler).serve_forever()
