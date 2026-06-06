import json

with open(
    "data/processed/sightings_2018_2024.geojson",
    encoding="utf-8"
) as f:
    data = json.load(f)

rows = []

for feature in data["features"]:

    p = feature["properties"]

    if p.get("year") != "2024":
        continue

    if p.get("city_norm") != "熊谷市":
        continue

    adults = p.get("adult_count_norm") or 0

    try:
        adults = int(adults)
    except:
        adults = 0

    rows.append({
        "facility": p.get("施設名称"),
        "address": p.get("住所"),
        "adults": adults,
    })

rows.sort(
    key=lambda x: x["adults"],
    reverse=True
)

for r in rows[:30]:
    print(
        r["adults"],
        r["facility"],
        r["address"]
    )