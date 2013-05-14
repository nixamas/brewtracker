import SimpleHTTPServer, SocketServer, json
from jsonencoder import build_json
            
class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print (" SELF DATA path "+ str(self.path) )
        form = {}
        if self.path.find('?') > -1:
            queryStr = self.path.split('?')[1]
            form = dict([queryParam.split('=') for queryParam in queryStr.split('&')])
            
        if self.path == "/datareadings.json":
            print ("Data readings request")
            self.send_response(200, 'OK')
            #self.send_header('Content-type', 'text/html')
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(str( build_json() ) )
            self.wfile.flush()
            #images = glob.glob('*.jpg')
            #rand = random.randint(0,len(images)-1)
            #imagestring = "<img src = \"" + images[rand] + "\" height = 1028 width = 786 align = \"right\"/> </body> </html>"
            #self.wfile.write(bytes(imagestring, 'UTF-8')
        else:
            print ("normal GET request")
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

theport = 1234
#Handler = http.server.SimpleHTTPRequestHandler
Handler = ServerHandler
pywebserver = SocketServer.TCPServer(("", theport), Handler)

print ("Python based web server. Serving at port" + str(theport))
pywebserver.serve_forever() 