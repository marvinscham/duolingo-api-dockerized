from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

hostName = "0.0.0.0"
serverPort = 7000


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/duo_user_info.json":
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()
            with open("duo_user_info.json", "rb") as file:
                self.wfile.write(file.read())
        elif self.path == "/health":
            self.send_response(418)
            self.send_header("Content-type", "beverage/tee")
            self.end_headers()
        else:
            self.send_response(403)
            self.end_headers()


def run_server():
    web_server = HTTPServer((hostName, serverPort), MyServer)

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")


logfile = open("duoserver.log", "w")
sys.stdout = logfile
sys.stdin = logfile
sys.stderr = logfile

run_server()
