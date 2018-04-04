import http.client
import json

headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", '/drug/label.json?&search=active_ingredient:"acetylsalicylic"&limit=100', None, headers)

r1 = conn.getresponse()
print(r1.status, r1.reason)

repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
repo = repos['results']
for i in range(len(repo)):
    print("Medication's id:", repo[i]['id'])
    try:
        print("-Manufacturer's name:", repo[i]['openfda']['manufacturer_name'][0])
    except KeyError:
        print("-Manufacturer's name not found")
