from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import start_http_server, Counter

hostName = "localhost"
serverPort = 8080
metricsPort = 8081
requestCounter = Counter("app_request_count", "total app http requests count")


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        requestCounter.inc()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8")
        )
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        start_http_server(metricsPort)
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
