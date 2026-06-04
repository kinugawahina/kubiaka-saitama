import json
import folium

INPUT = "data/processed/sightings_2018_2024.geojson"
OUTPUT = "maps/kubiaka_adult_top_2024.html"

TARGET_CITIES = {"加須市", "熊谷市", "行田市", "越谷市"}

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

features = [
    f for f in data["features"]
    if f["properties"].get("year") == "2024"
    and f["properties"].get("city_norm") in TARGET_CITIES
]

def adult_count(feature):
    value = feature["properties"].get("adult_count_norm") or 0
    try:
        return int(value)
    except Exception:
        return 0

features = sorted(features, key=adult_count, reverse=True)[:100]

m = folium.Map(
    location=[36.05, 139.45],
    zoom_start=10,
    tiles="OpenStreetMap",
)

for rank, f in enumerate(features, start=1):
    props = f["properties"]
    lon, lat = f["geometry"]["coordinates"]

    city = props.get("city_norm")
    address = props.get("住所") or props.get("詳細住所等") or ""
    facility = props.get("施設名称") or ""
    tree = props.get("tree_norm") or ""
    adults = adult_count(f)
    date = props.get("date_found_norm") or ""

    radius = min(24, max(6, 5 + adults ** 0.5))

    popup = f"""
    <b>#{rank} {city}</b><br>
    成虫頭数: {adults}<br>
    住所: {address}<br>
    施設: {facility}<br>
    樹種: {tree}<br>
    確認日: {date}
    """

    folium.CircleMarker(
        location=[lat, lon],
        radius=radius,
        popup=folium.Popup(popup, max_width=400),
        tooltip=f"#{rank} {city} / 成虫 {adults}",
        color="darkred",
        fill=True,
        fill_opacity=0.7,
    ).add_to(m)

m.save(OUTPUT)

print(f"features: {len(features)}")
print(f"created: {OUTPUT}")

print("\nTop 20:")
for rank, f in enumerate(features[:20], start=1):
    p = f["properties"]
    print(
        rank,
        p.get("city_norm"),
        adult_count(f),
        p.get("施設名称"),
        p.get("住所"),
    )