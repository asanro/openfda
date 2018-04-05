import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)

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
