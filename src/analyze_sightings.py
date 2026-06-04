import json
from collections import Counter

with open("data/processed/sightings_2018_2024.geojson", encoding="utf-8") as f:
    data = json.load(f)

features = data["features"]

print("総地点数:", len(features))

by_year = Counter(f["properties"].get("year") for f in features)
print("\n年度別:")
for year, count in sorted(by_year.items()):
    print(year, count)

by_city = Counter(f["properties"].get("市町村名") for f in features)
print("\n市町村別 top 20:")
for city, count in by_city.most_common(20):
    print(city, count)

by_tree = Counter(f["properties"].get("樹種") for f in features)
print("\n樹種 top 20:")
for tree, count in by_tree.most_common(20):
    print(tree, count)

recent = [
    f for f in features
    if f["properties"].get("year") == "2024"
]

print("\n2024年度地点数:", len(recent))

by_city_2024 = Counter(f["properties"].get("市町村名") for f in recent)
print("\n2024年度 市町村別 top 20:")
for city, count in by_city_2024.most_common(20):
    print(city, count)