import http.server
import http.client
import socketserver
import json  # importamos los módulos que posteriormente necesitremos

socketserver.TCPServer.allow_reuse_address = True

PORT = 8000 #puerto donde se lanza el server


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # Necesitamos un cliente para poder establecer conexión y acceder a la información demandada
    # definimos la función listdata de cliente para que se conecten al mismo recurso, las listas drug, company_name y warnings

    def listdata(self, limit):

        headers = {'User-Agent': 'http-client'}  #Las cabeceras indican a la página web quienes somos
        conn = http.client.HTTPSConnection("api.fda.gov") #Se establece conexión con el servidor
        conn.request("GET", '/drug/label.json?&limit=' + limit, None, headers) # Enviamos un mensaje de solicitud para obtener la informacion
        r1 = conn.getresponse()#Obtenemos la respuesta del servidor y guardamos la informacion en r1
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8") #decodificamos el mensaje obtenido (formato de trasformación unicode)
        conn.close()

        repos = json.loads(repos_raw)#Convertimos el objeto json a un lenguaje python, para que podamos trabajar con la información

        return repos

    def do_GET(self): #Cada vez que hay una peticion GET por HTTP, empieza a funcionar esta función. El recurso que nos solicitan se encuentra
        # en self.path

        #Esablecemos la respuesta y las cabeceras por defecto
        response = 200
        header1 = 'Content-type'
        header2 = 'text/html'

        if self.path == "/":
            with open("index.html") as f: #Abrimos el archivo html, lo leemos y lo guardamos en la variable html.
                html = f.read() #Este html coresponde a la pagina principal

        elif "listDrugs" in self.path: #Devuelve un html con todos los diferentes nombres de medicamentos disponibles en la pagina web
            param = self.path.split("?")[1]
            limit = param.split("=")[1] #Parametro introducido por el usuario que hay que pasar al cliente para que obtenga la información de openfda
            data = self.listdata(limit) #Invocamos la funcion listdata para obtener el diccionario del recurso solicitado y lo guardamos en data
            #Principio del html de la lista de medicamentos

            html = """<!doctype><html><body> 
            <h1>Requested Drug List</h2>
            <ul>"""

            try:
                for drug in data['results']: #Iteramos con un bucle por los elementos del diccionario data
                    if drug['openfda']: #Como la información que queremos esta dentro de openfda,
                    # nos aseguramos de que esta exista para que no se produzca un KeyError y poder añadir los datos al html anteriormente
                        html += "<li>" + drug['openfda']['generic_name'][0] + "</li>"
                    else: #Si el nombre del medicamento no está disponible devolverá su id
                        html += "<li>" + "Medication's name not available" + "</li>" + "- Drug ID: " + drug['id']
            except KeyError:
                print('Incorrect limit: must be integer or between 1-100')
                pass
            #Final del html
            html += "</ul></body></html>"

            #En los elif a continuación se repetirá el mismo proceso

        elif "searchDrug" in self.path:  # Devuelve un html con todos los medicamentos que contienen el mismo ingrediente activo en su formula
            param = self.path.split("?")[1]
            active_ingredient = param.split("=")[1] #Parametro introducido por el usuario que hay que pasar al cliente para que obtenga la informacion de openfda
            limit = 10

            #Este cliente establecerá conexión y accederá a la información requerida en searchdrug. Se conectará a un recurso
            #determinado (dependieno del ingrediente activo). El resto del cliente funciona igual que el que hemos definido anteriormente
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET",'/drug/label.json?&search=active_ingredient:' + active_ingredient + "&limit=" + str(limit),None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            data = json.loads(repos_raw)

            html = """<!doctype><html><body>
            <h1>All of the requested drugs below </h2>"""
            html += '<body>List of drugs with </body>' + active_ingredient.replace('+', ' ') + '<body> as their active ingredient:</body>'
            html += '<ul>'

            try:
                for drug in data['results']:
                    if drug['openfda']:
                        html += "<li>" + drug['openfda']['generic_name'][0] + "</li>"
                    else:
                        html += "<li>" + "Medication's name not available" + "</li>" + "- Drug ID: " + drug['id']
            except KeyError:
                html += '<body>No drugs found by the active ingredient: </body>' + active_ingredient
                pass
            html += "</ul></body></html>"

        elif "listCompanies" in self.path:  # Devuelve un html con todas las empresas que están en los fármacos devueltos por OpenFDA
            param = self.path.split("?")[1] #Dividimos por sus parametros
            limit = param.split("=")[1]
            data = self.listdata(limit)

            html = """<!doctype><html><body>
            <h1>Requested Company list </h2>
            <ul>"""

            try:
                for drug in data['results']:
                    if drug['openfda']:
                        html += "<li>" + drug['openfda']['manufacturer_name'][0] + "</li>"
                    else:
                        html += "<li>" + "Company not availabe" + "</li>"
            except KeyError:
                print('Incorrect limit, must be integer and beteween 1-100')
                pass

            html += "</ul></body></html>"

        elif "searchCompany" in self.path:  # Devuelve un html con todos los medicamentos que tienen el mismo fabricante
            param = self.path.split("?")[1] #se obtienen los parametros
            company_name = param.split("=")[1]
            limit =10

            # Este cliente establecerá conexión y accederá a la información requerida en searchcompany que se conectará a un recurso
            # determinado (dependieno del nombre del fabricante). El resto del cliente funciona igual que el que hemos definido anteriormente
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET",'/drug/label.json?&search=openfda.manufacturer_name:' + company_name + "&limit=" + str(limit),None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            data = json.loads(repos_raw)

            html = """<!doctype><html><body>
            <h1>All of the requested drugs below </h2>"""
            html += '<body>List of drugs with </body>' + company_name.replace('+', ' ') + '<body> as their Company:</body>'
            html += '<ul>'
            try:
                for drug in data['results']:
                    if drug['openfda']:
                        html += "<li>" + drug['openfda']['generic_name'][0] + "</li>"
                    else:
                        html += "<li>" + "Medication's name not available" + "</li>" + "-Drug ID: " + drug['id']
            except KeyError:
                html += '<body>No drugs found by the company name: </body>' + company_name
                pass
            html += "</ul></body></html>"

        elif "listWarnings" in self.path: #Devuelve un html con las advertencias de cada medicamento
            param = self.path.split("?")[1]
            limit = param.split("=")[1]
            data = self.listdata(limit)

            html = """<!doctype><html><body>
            <h1>Requested Warning list</h2>
            <ul>"""

            try:
                for drug in data['results']:
                    if 'warnings' in drug:
                        if drug['openfda']:
                            html += "<li>" + drug['openfda']['generic_name'][0] + "</li>" + '-' + drug['warnings'][0]
                        else:
                            html += "<li>" + "Medication's name not available" + "</li>" + "-Drug ID: " + drug['id']+ '<br>'
                            html += '-' + drug['warnings'][0]
                    else:
                        html += "<li>" + "Warnings not avaliable" + "</li>"
            except KeyError:
                print ('Incorrect limit, must be integer and between 1-100')
                pass

            html += "</ul></body></html>"

        elif 'secret' in self.path:
            response = 401
            header1 = 'WWW-Authenticate' #Esta cabecera define el método de autenticación que debería ser usado para tener acceso al contenido.
            header2 = 'Basic realm="Mi servidor"'
            self.send_error(401) #Envia una respuesta de error al cliente
            # en este caso el 401 especifica el error del http (una página no autorizada)

        elif 'redirect' in self.path: #Nos redireccionará a la pagina principal
            response = 302
            print("Redirect to homepage")
            header1 = 'Location' #Esta cabecera indica la URL a la que debe redirigir una página determinada.
            header2 = 'http://localhost:8000' #Url a la que redirige

        else: #En el caso de que el recurso proporcionado no se haya encontrado, se enviará un html de error advirtiéndolo
            response = 404
            html = '''<html>
            <head>
                <title>Error response</title>
            </head>
            <body>
                <h1>Error code: 404</h1>
            </body>
            <body>Message: Resource not found.</body><br>
            <body>Nothing matches the given URI.</body>
            </html>'''

        self.send_response(response)#Indicamos el estado OK mediante un mensaje
        self.send_header(header1, header2) # Colocamos las cabeceras necesarias para que el cliente entienda el contenido que enviamos (html)
        self.end_headers()
        if response == 200 or response == 404: #después de haber leido el codigo, si la respuesta ha sido 200 o 404 mandará el html correspondoente
            self.wfile.write(bytes(html, "utf8"))  # Se envía el mensaje html completo

        return


# El servidor comienza a aqui
# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)  # establecemos el socket del servidor para que espere a las peticiones de los clientes
print("serving at port", PORT)
try:
    httpd.serve_forever() # El servidor establece y recibe conexiones de los clientes
except KeyboardInterrupt: #Parará cuando el usuario lo decida
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
httpd.close()
