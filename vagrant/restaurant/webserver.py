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
            if self.path.endswith("/restaurants") or self.path.endswith("/restaurants/"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href='restaurants/new'>Add another restaurant</a>"
                output += "<br><br><br>"
                for restaurant in restaurants:
                    print restaurant.name
                    output += restaurant.name
                    output += "<br>"
                    output += "<a href='#'>Edit</a><br>"
                    output += "<a href='#'>Delete</a><br>"
                    output += "<br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new") or self.path.endswith("/restaurants/new/"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<head><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Create a New Restaurant</h2><input name="newRestaurant" type="text" placeholder="Restaurant Name"><input type="submit" value="Create"></form>'''
                output += "</head></body>"


                print "Navigated to Add Restaurant Page"
                self.wfile.write(output)
                return


        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new") or self.path.endswith("/restaurants/new/"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantName = fields.get('newRestaurant')
                addRestaurant = Restaurant(name = restaurantName[0])

                session.add(addRestaurant)
                session.commit()
                print "Adding Restaurant..."

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                print 'New restaurant, "%s", added to database!' % restaurantName[0]

        except:
            raise


def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHanlder)
        print "+-----------------------------------------------------------------------+"
        print "| Web server running... open localhost:%s/restaurants in your browser |" % port
        print "+-----------------------------------------------------------------------+"
        server.serve_forever()

    except KeyboardInterrupt:
        print " entered, stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()
