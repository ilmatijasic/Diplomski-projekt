import requests
from REST_API import Item
import json

url_file = "http://127.0.0.1:8000/file/"
url_cols = "http://127.0.0.1:8000/columns/"
url_recommend = "http://127.0.0.1:8000/recommend/"


input = ['sexy', 'low', '0', 'S', 'summer', 'o-neck', 'sleevless', 'empire', 'microfiber', 'chiffon', 'ruffles', 'animal']
data = {}

# Vraca riječnik sa imenima polja i njihovim tipovima
schema = Item.schema()['properties']

# Mijenja string u integer ili float
for count, i in enumerate(schema):
    # print(i,input[count])
    temp = input[count]
    if schema[i]["type"] == "number":
        temp = float(temp)
    elif schema[i]["type"] == "integer":
        temp = int(temp)
    data[i] = temp
headers = {}

print("Sending file...")
files = {'file': open(r'Dresses dataset/Attribute DataSet.xlsx', 'rb')}
response = requests.post(url_file, files=files)

print("Response: ")
print(response.json())

print("\nSending Request for column names...")
response = requests.request("GET", url_cols)

print("Response: ")
print(response.json())

# Slanje GET zahtjeva API
print("\nSending request for recommendation...")
response = requests.request("GET", url_recommend, headers=headers, json=data)

# Print poslani i primljeni json
print("Sent query: ")
print(json.dumps(data, indent=2))
print()
print("Got: ")
print(response.json())







