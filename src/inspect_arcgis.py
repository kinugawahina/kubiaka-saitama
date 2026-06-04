import requests
import json
import re

ITEM_ID = "8b5c7e9ba0cd4737ab886ca5c2236d1d"

url = f"https://www.arcgis.com/sharing/rest/content/items/{ITEM_ID}/data"
params = {"f": "json"}

r = requests.get(url, params=params, timeout=30)
r.raise_for_status()

text = r.text

matches = sorted(set(re.findall(r"https://[^\"']+FeatureServer[^\"']*", text)))

print(f"FeatureServer URLs: {len(matches)}")
for m in matches:
    print(m)

with open("data/raw/dashboard_data.json", "w", encoding="utf-8") as f:
    json.dump(r.json(), f, ensure_ascii=False, indent=2)

print("saved: data/raw/dashboard_data.json")
