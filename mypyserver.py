import http.server
import json
import socketserver
exData = {"firstName": "John","lastName": "Smith","age": 25,
                "address": {
                    "streetAddress": "21 2nd Street",
                    "city": "New York",
                    "state": "NY",
                    "postalCode": 10021
                }
            }
            
class ServerHandler(http.server.SimpleHTTPRequestHandler):
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
            self.wfile.write(bytes(str("{'firstname':'ryan', 'lastname':'nix'}"), 'UTF-8'))
            self.wfile.flush()
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