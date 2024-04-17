import requests
import json

url = f"https://api.potterdb.com/v1/books"
response = requests.get(url)
data = response.json()
    
with open("hpmain.json", 'w') as file:
    json.dump(data, file, indent=4)

data_1=data["data"]

for i in data_1:
    h1 = (i["attributes"]["slug"])
    new_h1 = h1.replace("-", " ")
    print(new_h1.title())