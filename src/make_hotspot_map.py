import json
import folium

INPUT = "data/processed/sightings_2018_2024.geojson"
OUTPUT = "maps/kubiaka_hotspots_2024.html"

HOT_CITIES = {
    "加須市",
    "熊谷市",
    "行田市",
    "鴻巣市",
    "本庄市",
    "北本市",
    "東松山市",
    "越谷市",
    "越生町",
    "深谷市",
    "川島町",
}

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

features = [
    f for f in data["features"]
    if f["properties"].get("year") == "2024"
    and f["properties"].get("city_norm") in HOT_CITIES
]

m = folium.Map(
    location=[36.05, 139.45],
    zoom_start=10,
    tiles="OpenStreetMap",
)

def radius(props):
    n = props.get("adult_count_norm") or 0
    try:
        n = int(n)
    except Exception:
        n = 0
    return min(16, max(5, 4 + n ** 0.5))

for f in features:
    props = f["properties"]
    lon, lat = f["geometry"]["coordinates"]

    city = props.get("city_norm")
    address = props.get("住所") or props.get("詳細住所等") or ""
    facility = props.get("施設名称") or ""
    tree = props.get("tree_norm") or ""
    adults = props.get("adult_count_norm") or 0
    date = props.get("date_found_norm") or ""

    popup = f"""
    <b>{city}</b><br>
    住所: {address}<br>
    施設: {facility}<br>
    樹種: {tree}<br>
    成虫頭数: {adults}<br>
    確認日: {date}
    """

    folium.CircleMarker(
        location=[lat, lon],
        radius=radius(props),
        popup=folium.Popup(popup, max_width=350),
        tooltip=f"{city} / 成虫 {adults}",
        color="red",
        fill=True,
        fill_opacity=0.65,
    ).add_to(m)

folium.LayerControl().add_to(m)
m.save(OUTPUT)

print(f"features: {len(features)}")
print(f"created: {OUTPUT}")