#
# Python HTTP/DataStreaming Server 
# Felipe Sousa Rocha, 1/8/2014
#

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import cgi
import urlparse
import sys
import json
import httpServerDatabase

HTTPHost = 'localhost'
HTTPPort = 8080

ext2conttype = {"jpg":  "image/jpeg",
                "jpeg": "image/jpeg",
                "png":  "image/png",
                "gif":  "image/gif",
                "js":   "",
                "html": "",
                "css":  ""}

def content_type(filename):
    return ext2conttype[filename[filename.rfind(".")+1:].lower()]

class Handler(BaseHTTPRequestHandler):
   
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)

        print self.path
        
        if self.path == "/":
            self.wfile.write('HTTP/1.0 200 OK\r\n')
            self.wfile.write("Content-Type: text/html\r\n\r\n")
            self.end_headers()
            sfile = open("./webApp/index.html", "r")
            messagez = sfile.read()
        elif self.path == "/update":
            self.wfile.write('HTTP/1.0 200 OK\r\n')
            self.wfile.write("Content-Type: application/json\r\n\r\n")
            self.end_headers()
            self.wfile.write(httpServerDatabase.GetRealtimeAirplaneList())
        else:
            print "passou"
            try:
                self.wfile.write('HTTP/1.0 200 OK\r\n')
                self.wfile.write("Content-Type: "+content_type(self.path)+"\r\n\r\n")
                self.end_headers()
                print content_type(self.path)
                sfile = open("./webApp/"+self.path, "r")
                messagez = sfile.read()
            except Exception:
                self.wfile.write('HTTP/1.0 404 NOT FOUND\r\n')
                self.wfile.write("Content-Type: text/html\r\n\r\n")
                self.end_headers()
                self.wfile.write("<center><h3>Nada foi encotrado</h3></center>")
            return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer((HTTPHost, HTTPPort), Handler)
    print 'Iniciando, use <Ctrl-C> to stop'
    server.serve_forever()


 
''' def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()
        
        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                self.wfile.write('\tUploaded %s as "%s" (%d bytes)\n' % \
                        (field, field_item.filename, file_len))
            else:
                # Regular form value
                #self.wfile.write('\t%s=%s\n' % (field, form[field].value))

                if field == "voice_input":
                   pass
return'''
