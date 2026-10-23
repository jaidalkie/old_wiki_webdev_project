# $ python3 -m http.server -b 127.0.0.42 8080
# $ python3 -m http.server -d /usr/lib/python3.8/
# terminate the http server with ctrl c
# $ mkdir cgi-bin/

# in {cgi-bin/} we have a python file, {hello.py}:

#!/usr/bin/env python3

# main imports
import articalgen # my artical generation program, to help fluff up the web app.
import sqlite3
import os # because there can be issues with opening files on the system, specifically all our html and css files.
from http.server import BaseHTTPRequestHandler # an object that handles our http requests
from http.server import HTTPServer # an server object to run this server.

import uuid # for gaining cookies from the client. important for identifying the client sessoins our program works with.

# most of these imports correlate to certain functions we have implemented in the "catched_propertys"
from functools import cached_property
from http.cookies import SimpleCookie
from urllib.parse import parse_qsl, urlparse

class the_server(BaseHTTPRequestHandler): 
    # the following cached property definitions simply allow
    # this program to agregate HTTP requests from the web app.

    # this requesthandler is not equiped for taking more then one number of requests.
    # this means that the server will only handle one client, i have decided to take 
    # simple approche, to avoid trying to implement "threading", or ways of unpacking 
    # numbered requests and numbered users. it means i will probably look at this challange 
    # being disributed for local host via downloads. 

    @cached_property # obtain the URL.
    def url(self):
        return urlparse(self.path)

    @cached_property # "parse_qsl" the query, as a peice of data thats then stored in a dictionary, as per the urllib.parse import.
    def query_data(self): # use this to keep a HTTP request
        return dict(parse_qsl(self.url.query))

    @cached_property 
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self): # specially for obtaining form data, it will run a "decode", then query it in a dictionary, as per the urllib.parse import.
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self): 
        return SimpleCookie(self.headers.get("Cookie"))

    def do_GET(self): # 
        global debug_screen
        global clients
        c = self.obtain_client()# identify the client so we can setup their web experiance.
        self.send_response(200) # adds a responce header to the header buffer, logging the accepted request.
        # dynamic file extention opening sequence
        content_types = {".html":"text/html",".css":"text/css"}
        _,ext = os.path.splitext(self.path)
        content_type = content_types.get(ext,"application/octet-stream") 
        self.send_header("Content-Type", "text/html") # adds the http header to the internal buffer. we are basically specifying the html files we send to the client. 

        if not any(cookie.startswith("client_id") for cookie in self.headers.get_all("Set-Cookie",[])):
            self.send_header("Set-Cookie", f"client_id={self.clid}; Path=/")
        self.end_headers() # once the headers are initulised, this indicates the end of the http headers in the responce. it then puts the headers into the "output stream" with "flush_headers()".
        # "wfile" contains the "output stream", for writing a responce back to the client.
        self.wfile.write((c["page"][((c["location"]).split("|"))[0]] ).encode("utf-8")) # write back a html string, this should become the web page.
        print(f"a GET:")

    def obtain_client(self):
        global debug_screen
        global clients

        # obtain client id.

        cookies = SimpleCookie(self.headers.get("Cookie"))
        if "client_id" in cookies:
            self.clid = cookies["client_id"].value # this is where we obtain from the cookies, a id for the client. with this identification, we know if we have a new client or not, and whether or not they need to register.
        else: # a case where this client doesn't have an id.
            self.clid = str(uuid.uuid4())

        # initulise the client if new.

        if self.clid not in clients:
            page = {}
            BASE = os.path.dirname(__file__)# this will be needed to correctly open our html files.
            html_files = ["page1.html", "page2.html", "page3.html", "page4.html", "page5.html"]
            for x in html_files:
                try:
                    page[x] = str(open(os.path.join(BASE, x)).read())
                except Exception as e:
                    page[x] = f"<h1>{x}: page not found, strange</h1>"
                    print(f"unable: {x} because: {e}")

            cur.execute(f"SELECT * FROM users WHERE client = '{self.clid}'")
            clients[self.clid] = {"page":page,
                                  "location":"page2.html" if cur.fetchone() else "page3.html",
                                  "account":""} # we can give our clients their own cookie data.
            print(f"created new client: {self.clid}")
        return clients[self.clid]
    
    def do_POST(self): # the post method can handle inputs from the html page, we make use of the "debug_screen" dictionary to archive inputs, the GET_.
        global debug_screen
        global clients
        self.get_debug()# here, this should always happen whenever resaving a POST, some interaction back from the client.
        c = self.obtain_client()
        if c["account"] == "admin":
            cur.execute(f"INSERT INTO articals (author, title, content, editing, image) VALUES ('admin','a secure,confidentual artical','friday','','');")

        try:
            # the main page
            if ((c["location"]).split("|"))[0] == "page1.html":
                # form filler:
                for x in list({"search","visit","update"}-set(debug_screen[len(debug_screen)-1]["form_data"].keys())):
                    debug_screen[len(debug_screen)-1]["form_data"][x] = ""
                # following code:
                insert = lambda con, con2, n: con[:n]+[con2]+con[n:]
                place = lambda pg, pl: insert(pg.split(pg[(pg).index(f"<{pl}>")+len(f"<{pl}>"):(pg).index(f"</{pl}>")]),pg[(pg).index(f"<{pl}>")+len(f"<{pl}>"):(pg).index(f"</{pl}>")],1)
                build = place(c["page"][((c["location"]).split("|"))[0]],"section") # begin

                build[1] = []
                if len((c["location"]).split("|")) > 1:
                    cur.execute(f"SELECT * FROM articals WHERE title LIKE '%{((c["location"]).split("|"))[1]}%'")
                    print("finding")
                else:
                    cur.execute(f"SELECT * FROM articals")

                for row in cur.fetchall():
                    build[1].append(f'''<header>
                    <form method="POST">
                        <label for = "that"> {(row)["title"]}, by {(row)["author"]}: </label> 
                        <input type="hidden" name="visit" value="{(row)["title"]}">
                        <button type="submit">visit</button>
                    </form>
                    <p>{((row)["content"])[:500]}</p>
                    </header>''')
                build[1] = "".join(build[1]) # end
                c["page"][c["location"]] = "".join(build) # end

                if not(debug_screen[len(debug_screen)-1]["form_data"]["visit"]) == "":
                    c["location"] ="page4.html|"+debug_screen[len(debug_screen)-1]["form_data"]["visit"]
                elif not(debug_screen[len(debug_screen)-1]["form_data"]["search"]) == "":
                    c["location"] ="page1.html|"+debug_screen[len(debug_screen)-1]["form_data"]["search"]


            # the login page
            elif c["location"] == "page2.html":
                # form filler:
                for x in list({"visit","username","password"}-set(debug_screen[len(debug_screen)-1]["form_data"].keys())):
                    debug_screen[len(debug_screen)-1]["form_data"][x] = ""
                # following code:

                if (debug_screen[len(debug_screen)-1]["form_data"]["visit"]) == "True":
                    c["location"] = "page1.html"
                    c["account"] = "admin"
                else: 
                    cur.execute(f"SELECT * FROM users WHERE username = '{(debug_screen[len(debug_screen)-1]["form_data"]["username"])}' AND password = '{(debug_screen[len(debug_screen)-1]["form_data"]["password"])}'")
                    if cur.fetchone():
                        c["location"] = "page1.html"
                        c["account"] = (debug_screen[len(debug_screen)-1]["form_data"]["username"])
                    else:
                        print(f"incorrect authentication: because:")
            # the registration page
            elif c["location"] == "page3.html":
                # form filler:
                for x in list({"email","username","password"}-set(debug_screen[len(debug_screen)-1]["form_data"].keys())):
                    debug_screen[len(debug_screen)-1]["form_data"][x] = ""
                # following code:

                try:
                    cur.execute(f"SELECT * FROM users WHERE username = '{(debug_screen[len(debug_screen)-1]["form_data"]["username"])}' OR password = '{(debug_screen[len(debug_screen)-1]["form_data"]["password"])}' OR email = '{(debug_screen[len(debug_screen)-1]["form_data"]["email"])}'")
                    if cur.fetchone():
                        print(f"the inputs: {cur.fetchone()}. already exist")
                    else:
                        cur.execute(f"INSERT INTO users (username, password, email, client, permission) VALUES ('{(debug_screen[len(debug_screen)-1]["form_data"]["username"])}','{(debug_screen[len(debug_screen)-1]["form_data"]["password"])}','{(debug_screen[len(debug_screen)-1]["form_data"]["email"])}','{self.clid}','read');")
                        c["location"] = "page2.html"
                except Exception as e:
                    print(f"incorrect inputs: because: {e}")
            # artical viewing page
            elif ((c["location"]).split("|"))[0] == "page4.html":
                # form filler:
                for x in list({"escape","edit","update"}-set(debug_screen[len(debug_screen)-1]["form_data"].keys())):
                    debug_screen[len(debug_screen)-1]["form_data"][x] = ""
                # following code:

                insert = lambda con, con2, n: con[:n]+[con2]+con[n:]
                place = lambda pg, pl: insert(pg.split(pg[(pg).index(f"<{pl}>")+len(f"<{pl}>"):(pg).index(f"</{pl}>")]),pg[(pg).index(f"<{pl}>")+len(f"<{pl}>"):(pg).index(f"</{pl}>")],1)
                cur.execute(f"SELECT * FROM articals WHERE title = '{((c["location"]).split("|"))[1]}'")
                row = cur.fetchone()
                
                build = place(c["page"][((c["location"]).split("|"))[0]], "section") # begin
                build[1] = []
                for x in (row["content"]).split("|"):
                    build[1].append(f'''<p>{x}</p>''')
                build[1] = "".join(build[1]) # end
                c["page"][((c["location"]).split("|"))[0]] = "".join(build) # end

                build = place(c["page"][((c["location"]).split("|"))[0]], "h1") # begin
                build[1] = [row["title"],]
                build[1] = "".join(build[1]) # end
                c["page"][((c["location"]).split("|"))[0]] = "".join(build) # end

                if (debug_screen[len(debug_screen)-1]["form_data"]["escape"]) == "True":
                    c["location"] = "page1.html"
                elif (debug_screen[len(debug_screen)-1]["form_data"]["edit"]) == "True":
                    c["location"] = "page5.html|"+((c["location"]).split("|"))[1]
            # artical editing page
            elif ((c["location"]).split("|"))[0] == "page5.html":
                # form filler:
                for x in list({"escape","edit","update"}-set(debug_screen[len(debug_screen)-1]["form_data"].keys())):
                    debug_screen[len(debug_screen)-1]["form_data"][x] = ""
                # following code:

                insert = lambda con, con2, n: con[:n]+[con2]+con[n:]
                place = lambda pg, pl: insert(pg.split(pg[(pg).index(f"<{pl}>")+len(f"<{pl}>"):(pg).index(f"</{pl}>")]),pg[(pg).index(f"<{pl}>")+len(f"<{pl}>"):(pg).index(f"</{pl}>")],1)
                cur.execute(f"SELECT * FROM articals WHERE title = '{((c["location"]).split("|"))[1]}'")
                row = cur.fetchone()
                
                build = place(c["page"][((c["location"]).split("|"))[0]], "section") # begin
                build[1] = [f'''<form method="POST">
                    <input type="hidden" name="escape" value="True">
                    <button type="submit">save and escape</button>
                    <textarea name="content" rows="50" cols="90">{row["content"]}</textarea>
                    </form>''',]
                build[1] = "".join(build[1]) # end
                c["page"][((c["location"]).split("|"))[0]] = "".join(build) # end

                build = place(c["page"][((c["location"]).split("|"))[0]], "h1") # begin
                build[1] = [row["title"],]
                build[1] = "".join(build[1]) # end
                c["page"][((c["location"]).split("|"))[0]] = "".join(build) # end

                if (debug_screen[len(debug_screen)-1]["form_data"]["escape"]) == "True":
                    cur.execute(f"UPDATE articals SET content='{debug_screen[len(debug_screen)-1]["form_data"]["content"]}' WHERE title='{((c["location"]).split("|"))[1]}'")
                    c["location"] = "page4.html|"+((c["location"]).split("|"))[1]
                    print('saved')

        except Exception as e:
            print(f"a error occured: because: {e}")

        self.do_GET()# to me, this is basically updating stuff on the client side, as if sending information, or refreshing the page.
        print(f"a POST:\n{",".join([f"\n {x}:{debug_screen[len(debug_screen)-1][x]}" for x in tuple((debug_screen[len(debug_screen)-1]).keys())])}")
        print(c["location"])

    def get_debug(self): # update a dictionary with attributes relevant to a http request. usefull for debugging, or may be used for the processing of inputs.
        global debug_screen
        debug_screen.append({
            "path": self.url.path,
            "query_data": self.query_data,
            "post_data": self.post_data.decode("utf-8"),
            "form_data": self.form_data,
            "cookies": {
                name: cookie.value
                for name, cookie in self.cookies.items()
            },
        })

# define the hostname, we have localhost, but it may be speficied as some ip address, such as mine which is also localhost.
hostname = "localhost"
# define the serverport, ive used the default port, this ensures that its localhost. at all costs ive also speficied this with the hostname as im cautios.
serverport = 8000
# both hostname and serverport represent a tuple (host,port), this is the client_address.
conn = sqlite3.connect("users.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS users;")
cur.execute("DROP TABLE IF EXISTS articals;")
cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            client TEXT NOT NULL,
            permission TEXT NOT NULL)""")
cur.execute(f"INSERT INTO users (username, password, email, client, permission) VALUES ('admin','abc123','None','None','admin');")
cur.execute("""CREATE TABLE IF NOT EXISTS articals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            editing TEXT NOT NULL,
            image TEXT NOT NULL)""")

cur.execute(f"INSERT INTO articals (author, title, content, editing, image) VALUES ('admin','a pecurliar artical','hello fellow readers, i expect nothing naughty. i can trust you to behave in the best interests for the wellbeing of our community.','','');")
for x in range(1,100):
    cur.execute(f"INSERT INTO articals (author, title, content, editing, image) VALUES ('staff','{(articalgen.generate(2)).split("|")[0]}','{articalgen.generate(1)}','','');") # 

# these variables have to be persistend per how the webapp runs, and do not associate with single clients.
clients = {}
debug_screen = []
# we could automatically setup the server with a command, like seen before. but in this case its nessasary to do it programmatically, i belive so that we can work with the request handler.
if __name__ == "__main__":
    # for the BaseHTTPRequstHandler(request, client_address, server), the client address is being served by (hostname, serverport) being defined in the server object.
    server = HTTPServer((hostname, serverport), the_server) # our request handler of choice is given as a argument to the server object we are creating.
    print(f"http://{hostname}:{serverport}") # a convenient url.

    # the serving of the server can be interrupted if a key is pressed, this is handled in the following.
    try:
        server.serve_forever() # i belive this makes the server object we made live and running.
        print("server running")
    except KeyboardInterrupt:
        pass

    server.server_close() # to tell the server to close, if the server was initualised in the command line, we would use Ctrl+c.
    print("server closed")
    conn.commit()
    conn.close()


# $ chmod +x cgi-bin/hello.py # if you want the script executable on unix like systems.
# $ python3 -m http.server --cgi # to start the server from the cgi switch optionally.
# http://0.0.0.0:8080/cgi-bin/hello.py # navigate to the following link to browse your html
# 

