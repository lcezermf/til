from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import start_http_server, Gauge
import time

host_name = "localhost"
server_port = 8080
metrics_port = 8081
request_is_progress = Gauge("app_requests_in_progress", "number of requests in progress")


class MyServer(BaseHTTPRequestHandler):

    @request_is_progress.track_inprogress
    def do_GET(self):
        
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

        time.sleep(5)


if __name__ == "__main__":
    webServer = HTTPServer((host_name, server_port), MyServer)
    print("Server started http://%s:%s" % (host_name, server_port))

    try:
        start_http_server(metrics_port)
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
