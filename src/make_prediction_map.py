import json
import folium

INPUT = "data/processed/sightings_2018_2024.geojson"
OUTPUT = "maps/kubiaka_prediction_2026.html"

TARGET_CITIES = {
    "加須市",
    "熊谷市",
    "行田市",
    "鴻巣市",
    "越谷市",
}

MIN_ADULTS = 100

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)


def adult_count(feature):
    value = feature["properties"].get("adult_count_norm") or 0
    try:
        return int(value)
    except Exception:
        return 0


def prediction_radius_m(adults):
    if adults >= 1000:
        return 2000
    if adults >= 500:
        return 1500
    if adults >= 100:
        return 1000
    return 500


features = [
    f for f in data["features"]
    if f["properties"].get("year") == "2024"
    and f["properties"].get("city_norm") in TARGET_CITIES
    and adult_count(f) >= MIN_ADULTS
]

features = sorted(features, key=adult_count, reverse=True)

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
    facility_type = props.get("施設区分") or ""
    tree = props.get("tree_norm") or ""
    adults = adult_count(f)
    date = props.get("date_found_norm") or ""
    radius_m = prediction_radius_m(adults)

    popup = f"""
    <b>#{rank} {city}</b><br>
    予測半径: {radius_m}m<br>
    成虫頭数: {adults}<br>
    施設区分: {facility_type}<br>
    施設: {facility}<br>
    住所: {address}<br>
    樹種: {tree}<br>
    確認日: {date}
    """

    # 2026予測圏
    folium.Circle(
        location=[lat, lon],
        radius=radius_m,
        color="blue",
        fill=True,
        fill_opacity=0.12,
        popup=folium.Popup(popup, max_width=420),
    ).add_to(m)

    # 2024発生中心点
    folium.CircleMarker(
        location=[lat, lon],
        radius=min(18, max(6, 4 + adults ** 0.5 / 3)),
        color="darkred",
        fill=True,
        fill_opacity=0.8,
        tooltip=f"#{rank} {city} / 成虫 {adults}",
        popup=folium.Popup(popup, max_width=420),
    ).add_to(m)

m.save(OUTPUT)

print(f"seed points: {len(features)}")
print(f"created: {OUTPUT}")

print("\nPrediction seed points:")
for rank, f in enumerate(features[:30], start=1):
    p = f["properties"]
    print(
        rank,
        p.get("city_norm"),
        adult_count(f),
        p.get("施設名称"),
        p.get("住所") or p.get("詳細住所等"),
    )