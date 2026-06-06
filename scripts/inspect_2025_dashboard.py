import requests
import json
import re

ITEM_ID = "e51e7ae7c69440bebdb8e7a052c6b661"

url = f"https://www.arcgis.com/sharing/rest/content/items/{ITEM_ID}/data"

r = requests.get(
    url,
    params={"f": "json"},
    timeout=30
)

r.raise_for_status()

data = r.json()

with open(
    "data/raw/dashboard_2025.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

text = json.dumps(data, ensure_ascii=False)

ids = sorted(
    set(
        re.findall(
            r"\b[a-f0-9]{32}\b",
            text
        )
    )
)

print("item ids:")
for i in ids:
    print(i)