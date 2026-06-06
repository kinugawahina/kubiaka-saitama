import json
from collections import Counter

from sklearn.cluster import DBSCAN
import numpy as np

INPUT = "data/processed/sightings_2018_2024.geojson"

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

features = [
    f for f in data["features"]
    if (
        f["properties"].get("year") == "2024"
        and f["properties"].get("city_norm") == "熊谷市"
    )
]

coords = np.array([
    [
        f["geometry"]["coordinates"][1],  # lat
        f["geometry"]["coordinates"][0],  # lon
    ]
    for f in features
])

# 約500m程度
kms_per_radian = 6371.0088
epsilon = 0.5 / kms_per_radian

db = DBSCAN(
    eps=epsilon,
    min_samples=3,
    algorithm="ball_tree",
    metric="haversine",
)

labels = db.fit_predict(np.radians(coords))

for feature, label in zip(features, labels):
    feature["properties"]["cluster_id"] = int(label)

counts = Counter(labels)

print("clusters")
for cid, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    print(cid, count)

from collections import defaultdict

cluster_adults = defaultdict(int)
cluster_count = defaultdict(int)

for feature in features:
    cid = feature["properties"]["cluster_id"]

    adults = feature["properties"].get("adult_count_norm") or 0

    try:
        adults = int(adults)
    except:
        adults = 0

    cluster_adults[cid] += adults
    cluster_count[cid] += 1

print("\nCluster Summary")

for cid in sorted(cluster_count.keys()):
    print(
        cid,
        "sites=", cluster_count[cid],
        "adults=", cluster_adults[cid],
    )