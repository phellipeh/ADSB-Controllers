from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import cgi
import urlparse

HTTPHost = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
HTTPPort = 8080 # Maybe set this to 9000.


#httpserverstart

#httpdatasendhttppage

class Handler(BaseHTTPRequestHandler):
    
    def do_POST(self):
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
        #self.wfile.write('Client: %s\n' % str(self.client_address))
        #self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
        #self.wfile.write('Path: %s\n' % self.path)
        #self.wfile.write('Form data:\n')
        
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
                
        return

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        '''message_parts = [
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                'HEADERS RECEIVED:',
                ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        '''
        #self.send_response(200, "Content-Type: text/html")
        self.wfile.write('HTTP/1.0 200 OK\r\n')


        if ".html" in self.path: 
            self.wfile.write("Content-Type: text/html\r\n\r\n")

        if ".js" in self.path: 
            self.wfile.write("Content-Type: text/html\r\n\r\n")

        if ".css" in self.path: 
            self.wfile.write("Content-Type: text/html\r\n\r\n")

        if ".png" in self.path: 
            self.wfile.write("Content-Type: text/html\r\n\r\n")

        if ".jpg" in self.path: 
            self.wfile.write("Content-Type: image/jpg\r\n\r\n")

        self.end_headers()
        arq = self.path
        messagez = ""

        self.wfile.write('Client: %s\n' % str(self.client_address))
        self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
        self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write('Form data:\n')

        if self.path == "/update":
                self.wfile.write('Update')
        if self.path == "/":
                self.wfile.write('Main')
        
        try:
            sfile = open("."+arq, "r")
            messagez = sfile.read()
        except Exception:
            message="nao achou: "+arq + " " + str(Exception)
        self.wfile.write(messagez)
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer((HTTPHost, HTTPPort), Handler)
    print 'Iniciando, use <Ctrl-C> to stop'
    server.serve_forever()

#httpDataStreaming
