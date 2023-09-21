from http.server import BaseHTTPRequestHandler, HTTPServer
import json
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
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response_content = {
                "code": 200,
                "message": "I'm alive!"
            }
            response_json = json.dumps(response_content)
            self.wfile.write(response_json.encode("utf-8"))

        else:
            self.send_response(403)
            self.end_headers()


def run_server():
    print("Server started.")
    web_server = HTTPServer((hostName, serverPort), MyServer)

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")


run_server()
