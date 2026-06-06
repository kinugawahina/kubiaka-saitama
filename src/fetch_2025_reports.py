import json
import requests

URL = "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/クビアカツヤカミキリ発見大調査公開用/FeatureServer/0"

r = requests.get(
    f"{URL}/query",
    params={
        "f": "geojson",
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
    },
    timeout=60,
)

r.raise_for_status()
data = r.json()

for feature in data.get("features", []):
    props = feature.setdefault("properties", {})
    props["year"] = "2025"
    props["source_type"] = "citizen_report_2025"
    props["source_layer"] = URL

with open("data/processed/reports_2025.geojson", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("features:", len(data.get("features", [])))
print("saved: data/processed/reports_2025.geojson")

if data.get("features"):
    print("\nfields:")
    for k, v in data["features"][0]["properties"].items():
        print(f"{k}: {v}")