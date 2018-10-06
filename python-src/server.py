import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import controller

HOST_NAME = 'localhost'
PORT_NUMBER = 3001

class ReqHandler(BaseHTTPRequestHandler):
    def initiateController(self):
        self.controller = controller.Controller()
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/prediction': {'status': 200}
        }

        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond({'status': 500})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if (self.path == '/prediction'):
            content = self.controller.createAvailabilityPredictionForAllStations()
        else:
            content = 'Request path malformed or not defined.'
        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)
       

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ReqHandler)
    ReqHandler.initiateController(ReqHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))