import http.client
import json

headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", '/drug/label.json?&search=active_ingredient:"acetylsalicylic"&limit=100', None, headers)

r1 = conn.getresponse()
if r1.status == 404:
    print("Resource not found")
    exit(1)
print(r1.status, r1.reason)

repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
data = repos['results']
for i in range(len(data)):
    print("Medication's id:", data[i]['id'])
    try:
        print("-Manufacturer's name:", data[i]['openfda']['manufacturer_name'][0])
    except KeyError:
        print("-Manufacturer's name not found")
