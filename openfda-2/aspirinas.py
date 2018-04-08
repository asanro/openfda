import http.client
import json
#Necesitamos un cliente para poder establecer conexión y acceder a la información demandada
headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")#Se establece conexión con el servidor
conn.request("GET", '/drug/label.json?&search=active_ingredient:"acetylsalicylic"&limit=100', None, headers) #Utilizamos request y GET para
#obtener la información demandada. En este caso hay que añadir la función search para que pueda buscar todos los fabricantes que utilizan aspirinas
#entre los 100 medicamentos proporcionados por el limit=100

r1 = conn.getresponse()#Guardamos toda la información obtenida en una variable
if r1.status == 404:#Añadimos un if por si en el caso de que el recurso proporcionado no se haya encontrado, se imprima un mensaje advirtiéndolo
    print("Resource not found")
    exit(1)
print(r1.status, r1.reason)#imprimimos el estado de la conexion. 200OK si la conexión se ha establecido correctamente

repos_raw = r1.read().decode("utf-8")#decodificamos el mensaje obtenido
conn.close()

repos = json.loads(repos_raw)#Convertimos el objeto json a un lenguaje python, para que podamos trabajar con la información
data = repos['results'] #Guardamos en la variable la información que queremos, es decir, la información de cada medicamento
for i in range(len(data)): #Utilizamos un bucle for para iterar sobre los elementos de los medicamentos
    print("Medication's id:", data[i]['id']) #Imprimimos los id de cada medicamento por el que se va iterando
    if data[i]['openfda']: #Condicionamos que el elemento de data tenga el campo openfda, ya que no todos ellos lo tienen, para que no salte un KeyError y
        #se pueda acceder al nombre del fabricante
        print("-Manufacturer's name:", data[i]['openfda']['manufacturer_name'][0]) #Imprimimos el nombre del fabricante
    else: #Añadimos un else para todos aquellos elementos en los que no exista openfda o no haya ningún valor.
        print("-Manufacturer's name not found")
