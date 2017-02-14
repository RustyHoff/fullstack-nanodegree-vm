from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHanlder(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = session.query(Restaurant).all()

                output = ""
                output += "<html><body>"

                for restaurant in restaurants:
                    print restaurant.name
                    output += "<h1>" + restaurant.name + "</h1>\n"

                output += "</body></html>"
                self.wfile.write(output)
                print restaurant.name
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHanlder)
        print "+-----------------------------------------------------------------------+"
        print "| Web server running... open localhost:%s/restaurants in your browser |" % port
        print "+-----------------------------------------------------------------------+"
        server.serve_forever()

    except KeyboardInterrupt:
        print "\n^C entered, stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()
