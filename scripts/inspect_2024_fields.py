import requests
from pprint import pprint

url = "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/クビアカ2024発生確認/FeatureServer/0"

r = requests.get(
    url,
    params={"f": "json"},
    timeout=30
)

data = r.json()

print("FIELDS")
for field in data["fields"]:
    print(field["name"])