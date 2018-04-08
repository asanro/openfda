import http.client
import json #importamos los módulos que posteriormente necesitremos

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")  #Se establece conexión con el servidor
conn.request("GET", "/drug/label.json", None, headers) #Utilizamos request y GET para obtener la información demandada.
#Al no establecer ningún limit, la cantidad de medicamentos que devolverá por defecto es una.
r1 = conn.getresponse() #Guardamos toda la información obtenida en una variable

if r1.status == 404:#Añadimos un if por si en el caso de que el recurso proporcionado no se
            #haya encontrado, se imprima un mensaje advirtiéndolo
    print("Resource not found")
    exit(1)
print(r1.status, r1.reason)

repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)#Convertimos el objeto json a un lenguaje python, para que podamos trabajar con la información

data = repos['results'][0] #Guardamos en la variable data la información que queremos para trabajar con ella posteriormente
print("The medication's id is", data['id']+"; its purpose:", data['purpose'][0]+"; and the manufacturer's name is", data['openfda']['manufacturer_name'][0])
#Imprimimos por pantalla el id, su propósito y el nombre del fabricante del medicamento