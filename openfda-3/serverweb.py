import http.server
import socketserver
import http.client
import json

PORT = 8080

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", '/drug/label.json?limit=10', None, headers)

        r1 = conn.getresponse()
        if r1.status == 404:
            print("Resource not found")
            exit(1)
        print(r1.status, r1.reason)

        repos_raw = r1.read().decode("utf-8")
        conn.close()
        list = []
        repos = json.loads(repos_raw)
        data = repos['results']
        for i in range(len(data)):
            try:
                list.append(data[i]['openfda']['generic_name'][0])
            except KeyError:
                print("Medication's name not found")

        content = """
        <!doctype>
        <html>
        <h1>All of requested medication below </h2>
        <ul>"""
        for i in list:
            content+="<p>"+i+"</p>"
        content += "</ul></html>"

        self.wfile.write(bytes(content, "utf8"))
        print("File served!")
        return


Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
httpd.close()