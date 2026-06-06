import requests
import json

ITEM_ID = "025e1975b68248f3b6cb201254df9815"

meta_url = f"https://www.arcgis.com/sharing/rest/content/items/{ITEM_ID}"
data_url = f"https://www.arcgis.com/sharing/rest/content/items/{ITEM_ID}/data"

for name, url in [("meta", meta_url), ("data", data_url)]:
    r = requests.get(url, params={"f": "json"}, timeout=30)
    r.raise_for_status()

    out = f"data/raw/2025_{ITEM_ID}_{name}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(r.json(), f, ensure_ascii=False, indent=2)

    print(f"saved: {out}")

    if name == "meta":
        j = r.json()
        print("title:", j.get("title"))
        print("type:", j.get("type"))
        print("url:", j.get("url"))