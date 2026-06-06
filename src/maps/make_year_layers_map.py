import json
import folium

INPUT = "data/processed/sightings_2018_2024.geojson"
OUTPUT = "maps/kubiaka_year_layers.html"

COLORS = {
    "2018": "blue",
    "2019": "cadetblue",
    "2020": "green",
    "2021": "orange",
    "2022": "red",
    "2023": "darkred",
    "2024": "purple",
}

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

m = folium.Map(
    location=[36.0, 139.45],
    zoom_start=9,
    tiles="OpenStreetMap",
)

for year, color in COLORS.items():
    group = folium.FeatureGroup(
        name=f"{year}年度",
        show=(year == "2024"),
    )

    features = [
        f for f in data["features"]
        if f["properties"].get("year") == year
    ]

    for f in features:
        p = f["properties"]
        lon, lat = f["geometry"]["coordinates"]

        city = p.get("city_norm") or ""
        facility = p.get("施設名称") or ""
        address = p.get("住所") or p.get("詳細住所等") or ""
        tree = p.get("tree_norm") or ""
        adults = p.get("adult_count_norm") or 0
        date = p.get("date_found_norm") or ""

        popup = f"""
        <b>{year}年度</b><br>
        市町村: {city}<br>
        施設: {facility}<br>
        住所: {address}<br>
        樹種: {tree}<br>
        成虫頭数: {adults}<br>
        確認日: {date}
        """

        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color=color,
            fill=True,
            fill_opacity=0.65,
            popup=folium.Popup(popup, max_width=380),
            tooltip=f"{year} / {city}",
        ).add_to(group)

    group.add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

m.save(OUTPUT)

print("created:", OUTPUT)