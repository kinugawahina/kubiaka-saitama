import json
from pprint import pprint

with open(
    "data/processed/sightings_2018_2024.geojson",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)

print("feature count:", len(data["features"]))

first = data["features"][0]

print("\ngeometry:")
pprint(first["geometry"])

print("\nproperties:")
for k, v in first["properties"].items():
    print(f"{k}: {v}")