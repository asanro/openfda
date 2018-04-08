import http.client
import json
#explicar todo xd
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")  #Se establece conexión con el servidor
conn.request("GET", "/drug/label.json?limit=10", None, headers)#Utilizamos request y GET para obtener la información demandada.
#Establecemos un limit=10 para que se extraigan solo los 10 medicamentos demandados
r1 = conn.getresponse() #Guardamos toda la información obtenida en una variable
if r1.status == 404: #Añadimos un if por si en el caso de que el recurso proporcionado no se
            #haya encontrado, se imprima un mensaje advirtiéndolo
    print("Resource not found")
    exit(1)
print(r1.status, r1.reason)

repos_raw = r1.read().decode("utf-8") #decodificamos la información obtenida
conn.close()

repos = json.loads(repos_raw) #Convertimos el objeto json a un lenguaje python, para que podamos trabajar con la información
data = repos['results'] #Guardamos en la variable data la información que queremos para trabajar con ella posteriormente
for i in range(len(data)): #Con un bucle for iteramos sobre los medicamentos guardados en data
    print("Medication's id:", data[i]['id']) #imprimimos por pantalla los id de cada medicamento
