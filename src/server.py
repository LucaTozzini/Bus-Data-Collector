from http.server import BaseHTTPRequestHandler, HTTPServer

from middleware.serverUtil import *

staticPath = './public'

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Send a response back to the client with an index.html file as the response body
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('public/index.html', 'rb') as file:
                response = file.read()
                self.wfile.write(response)

        elif self.path.startswith('/AI'):
            query = getQuery(self.path)
            params = getParams('/AI/date/:date', self.path)
            print(params)
            print(query)
            
            if params == 'mismatch':
                self.send_error(404)
                
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(str(params).encode())

        else:
            staticFolder(staticPath, self)

def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=100):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
