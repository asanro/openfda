import http.server
import socketserver
import http.client
import json #importamos los módulos que posteriormente necesitremos

PORT = 8000 #Asignamos el puerto donde se lanza el servidor
socketserver.TCPServer.allow_reuse_address = True
#Definimos una clase que hereda los metodos de BaseHTTPRequestHandler.
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200) #Indicamos el estado OK mediante un mensaje
        # Colocamos las cabeceras necesarias para que el cliente entienda el contenido que enviamos
        # (que será HTML)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        #Necesitamos un cliente para poder establecer conexión y acceder a la información demandada
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov") #Se establece conexión con el servidor
        conn.request("GET", '/drug/label.json?limit=100', None, headers) #Utilizamos request y GET para
        #obtener la información demandada. Utilizamos limit=100 para que obtenga la información de ese numero de medicamentos

        r1 = conn.getresponse() #Guardamos toda la información obtenida en una variable
        if r1.status == 404: #Añadimos un if por si en el caso de que el recurso proporcionado no se
            #haya encontrado, se imprima un mensaje advirtiéndolo
            print("Resource not found")
            exit(1)
        print(r1.status, r1.reason) #imprimimos el estado de la conexion. 200OK si la conexión se ha
        #establecido correctamente

        repos_raw = r1.read().decode("utf-8") #decodificamos el mensaje obtenido
        conn.close() #cerramos la conexión
        list = [] #Creamos una lista vacia para guardar toda la informacion obtenida
        repos = json.loads(repos_raw) #Convertimos el objeto json a un lenguaje python, para que podamos
        #trabajar con la información
        data = repos['results'] #Guardamos en la variable la información que queremos
        for i in range(len(data)): #Iteramos sobre todos los elementos de la variable
            if data[i]['openfda']: #Como la información que queremos esta dentro de openfda, establecemos
                #esa condición para que no se produzca un KeyError y se pueda añadir a la lista a continuación
                #la información demandada
                list.append(data[i]['openfda']['generic_name'][0])
                #Añadimos a la lista los elementos de data que correspondan al nombre del medicamento con
                #la funcion append
                if len(list)==10: #Como el ejercicio pedia una lista de 10 medicamentos, condicionamos que
                    #si ya se han guardado un total de 10 elementos en la lista, el for pare de iterar sobre
                    #los elementos de data, salga y continúe leyendo el resto del código
                    break
            else: #En el caso de que el elemento de data sobre el que se esta iterando, no tenga el
                #campo requerido para poder añadirlos a la lista, imprimimos un mensaje advirtiédolo
                print("Medication's name not found")

        #A continuación creamos el html,en el cual, mediante un bucle for introducimos los medicamentos que
        #han sido guardados en la lista anteriormente.
        content = """
        <!doctype>
        <html>
        <h1>All of requested medication below </h2>
        <ol>"""
        for i in list:
            content+="<li>"+i+"</li>"
        content += "</ol></html>"

        self.wfile.write(bytes(content, "utf8")) # Se envía el mensaje html completo
        print("File served!")
        return

# El servidor comienza a aqui
# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler) #establecemos el socket del servidor para que espere
#las conexiones de los clientes
print("serving at port", PORT)
try:
    httpd.serve_forever() #El servidor establece y recibe conexiones de los clientes
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
httpd.close()