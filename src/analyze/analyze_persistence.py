import json
from collections import defaultdict

INPUT = "data/processed/sightings_2018_2024.geojson"

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

features = data["features"]

years = [str(y) for y in range(2018, 2025)]

city_year_counts = defaultdict(lambda: defaultdict(int))
city_year_adults = defaultdict(lambda: defaultdict(int))

for f in features:
    p = f["properties"]

    year = p.get("year")
    city = p.get("city_norm") or "不明"

    if year not in years:
        continue

    city_year_counts[city][year] += 1

    adults = p.get("adult_count_norm") or 0
    try:
        adults = int(adults)
    except Exception:
        adults = 0

    city_year_adults[city][year] += adults


def classify(counts):
    active_years = [y for y in years if counts.get(y, 0) > 0]

    if not active_years:
        return "no_data"

    if len(active_years) == 1:
        return "single_year"

    first = active_years[0]
    last = active_years[-1]

    recent = counts.get("2024", 0)
    prev = counts.get("2023", 0)

    if recent > 0 and prev == 0:
        return "new_or_reappeared"

    if recent >= prev * 2 and recent >= 10:
        return "rapid_growth"

    if recent > 0 and len(active_years) >= 4:
        return "established"

    if recent == 0 and prev > 0:
        return "declining_or_absent"

    return "intermittent"


rows = []

for city in sorted(city_year_counts.keys()):
    counts = city_year_counts[city]
    adults = city_year_adults[city]

    row = {
        "city": city,
        "class": classify(counts),
        "total_sites": sum(counts.values()),
        "total_adults": sum(adults.values()),
    }

    for y in years:
        row[f"sites_{y}"] = counts.get(y, 0)
        row[f"adults_{y}"] = adults.get(y, 0)

    rows.append(row)

rows.sort(
    key=lambda r: (
        r["class"] != "rapid_growth",
        -r["sites_2024"],
        -r["total_adults"],
    )
)

print("市町村別 定着・増殖フェーズ")
print()

for r in rows:
    print(
        r["city"],
        r["class"],
        "sites_2023=", r["sites_2023"],
        "sites_2024=", r["sites_2024"],
        "adults_2024=", r["adults_2024"],
    )