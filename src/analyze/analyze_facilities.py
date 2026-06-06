import json
from collections import Counter

with open(
    "data/processed/sightings_2018_2024.geojson",
    encoding="utf-8"
) as f:
    data = json.load(f)

features = [
    f for f in data["features"]
    if f["properties"].get("year") == "2024"
]

facility_counter = Counter()
facility_adults = Counter()

for f in features:
    p = f["properties"]

    facility = p.get("施設区分") or "不明"

    adults = p.get("adult_count_norm") or 0

    try:
        adults = int(adults)
    except Exception:
        adults = 0

    facility_counter[facility] += 1
    facility_adults[facility] += adults

print("=== 件数ランキング ===")
for name, count in facility_counter.most_common():
    print(f"{name}: {count}")

print("\n=== 成虫頭数ランキング ===")
for name, count in facility_adults.most_common():
    print(f"{name}: {count}")