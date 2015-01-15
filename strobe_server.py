import os
import re
import subprocess
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path == "/":
               print "Getting root"
               self.path = "/index.html";

            print "Request: " + self.path


            cmd = 'alarms find -u CRITICAL -a "atlas .*" -o 0 --count'
            print  "Execution command:" + cmd

            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                 stderr=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode != 0:
                print  'Failed code: ' + str(p.returncode) + '\ncmd: ' + cmd + '\nstdout: ' + out + '\nstderr: ' + err
                self.send_error(500,'Error: %s' % out)
                return

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(out)
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

def main():
    try:
        server = HTTPServer(('', 8080), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
