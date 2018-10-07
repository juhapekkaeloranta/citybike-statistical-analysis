import json
import time
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import controller
import constants

HOST_NAME = 'localhost'
PORT_NUMBER = 3001

class ReqHandler(BaseHTTPRequestHandler):
    stationRegex = re.compile('/prediction/\d+')
    stationHourRegex = re.compile('/prediction/\d+/\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ')
    
    def initiateController(self):
        self.controller = controller.Controller()
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if (self.stationHourRegex.match(self.path)):
            stationid = self.path.split('/')[2]
            timestamp = self.path.split('/')[3]
            if (int(stationid) in constants.stationIds):
                self.respond({'status': 200})
            else:
                self.respond({'status': 500})
        elif (self.stationRegex.match(self.path)):
            stationid = self.path.split('/')[2]
            if (int(stationid) in constants.stationIds):
                self.respond({'status': 200})
            else:
                self.respond({'status': 500})
        elif (self.path == '/prediction'):
            self.respond({'status': 200})
        else:
            self.respond({'status': 500})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if (self.stationHourRegex.match(self.path)):
            stationid = self.path.split('/')[2]
            timestamp = self.path.split('/')[3]
            if (int(stationid) in constants.stationIds):
                # A time not in the next 24 h will return empty array
                content = self.controller.getAvailabilityPredictionForOneStationHour(stationid, timestamp)
            else:
                content = 'Unknown station id.'
        elif (self.stationRegex.match(self.path)):
            stationid = self.path.split('/')[2]
            if (int(stationid) in constants.stationIds):
                content = self.controller.getAvailabilityPredictionForOneStation(stationid)
            else:
                content = 'Unknown station id.'
        elif (self.path == '/prediction'):
            content = self.controller.getAvailabilityPredictionForAllStations()
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
    print('\n', time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('\n', time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))