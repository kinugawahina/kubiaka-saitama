import json
from collections import defaultdict

INPUT = "data/processed/sightings_2018_2024.geojson"

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

sites = defaultdict(int)
adults = defaultdict(int)

for feature in data["features"]:

    p = feature["properties"]

    if p.get("year") != "2024":
        continue

    city = p.get("city_norm") or "不明"

    sites[city] += 1

    n = p.get("adult_count_norm") or 0

    try:
        n = int(n)
    except Exception:
        n = 0

    adults[city] += n

rows = []

for city in sites:

    count = sites[city]
    adult_total = adults[city]

    rows.append({
        "city": city,
        "sites": count,
        "adults": adult_total,
        "adults_per_site": round(
            adult_total / count,
            2
        )
    })

print("\n=== 地点数ランキング ===\n")

for r in sorted(
    rows,
    key=lambda x: x["sites"],
    reverse=True
)[:20]:

    print(
        f"{r['city']:10}",
        f"sites={r['sites']:4}",
        f"adults={r['adults']:6}",
        f"per_site={r['adults_per_site']}"
    )

print("\n=== 成虫数ランキング ===\n")

for r in sorted(
    rows,
    key=lambda x: x["adults"],
    reverse=True
)[:20]:

    print(
        f"{r['city']:10}",
        f"sites={r['sites']:4}",
        f"adults={r['adults']:6}",
        f"per_site={r['adults_per_site']}"
    )

print("\n=== 1地点あたり成虫数ランキング ===\n")

for r in sorted(
    rows,
    key=lambda x: x["adults_per_site"],
    reverse=True
)[:20]:

    if r["sites"] < 5:
        continue

    print(
        f"{r['city']:10}",
        f"sites={r['sites']:4}",
        f"adults={r['adults']:6}",
        f"per_site={r['adults_per_site']}"
    )