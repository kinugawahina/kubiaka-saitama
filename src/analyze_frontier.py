import json
import numpy as np
from sklearn.neighbors import BallTree

with open(
    "data/processed/sightings_2018_2024.geojson",
    encoding="utf-8"
) as f:
    data = json.load(f)

features = data["features"]

f2018 = [
    f for f in features
    if f["properties"].get("year") == "2018"
]

f2024 = [
    f for f in features
    if f["properties"].get("year") == "2024"
]

coords2018 = np.array([
    [
        f["geometry"]["coordinates"][1],
        f["geometry"]["coordinates"][0],
    ]
    for f in f2018
])

coords2024 = np.array([
    [
        f["geometry"]["coordinates"][1],
        f["geometry"]["coordinates"][0],
    ]
    for f in f2024
])

tree = BallTree(
    np.radians(coords2018),
    metric="haversine"
)

dist, idx = tree.query(
    np.radians(coords2024),
    k=1
)

km = dist[:, 0] * 6371

results = []

for feature, d in zip(f2024, km):
    p = feature["properties"]

    results.append({
        "city": p.get("city_norm"),
        "facility": p.get("施設名称"),
        "distance_km": float(d),
        "adults": p.get("adult_count_norm") or 0,
    })

results.sort(
    key=lambda x: x["distance_km"],
    reverse=True
)

print("Top frontier sites")

for r in results[:50]:
    print(
        round(r["distance_km"], 2),
        r["city"],
        r["facility"],
        r["adults"]
    )