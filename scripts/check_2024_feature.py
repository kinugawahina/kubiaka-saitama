import json
from pprint import pprint

with open(
    "data/processed/sightings_2018_2024.geojson",
    encoding="utf-8"
) as f:
    data = json.load(f)

feature_2024 = next(
    f for f in data["features"]
    if f["properties"]["year"] == "2024"
)

pprint(feature_2024["properties"])