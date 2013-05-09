import http.server
import socketserver

class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        print (" SELF DATA path "+ str(self.path) )
        if self.path == "/datareadings.json":
            print ("Data readings request")
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(bytes("{readingscount:'4', test:'data'}", 'UTF-8'))
            #images = glob.glob('*.jpg')
            #rand = random.randint(0,len(images)-1)
            #imagestring = "<img src = \"" + images[rand] + "\" height = 1028 width = 786 align = \"right\"/> </body> </html>"
            #self.wfile.write(bytes(imagestring, 'UTF-8')
        else:
            print ("normal GET request")
            http.server.SimpleHTTPRequestHandler.do_GET(self)

theport = 1234
#Handler = http.server.SimpleHTTPRequestHandler
Handler = ServerHandler
pywebserver = socketserver.TCPServer(("", theport), Handler)

print ("Python based web server. Serving at port" + str(theport))
pywebserver.serve_forever() 