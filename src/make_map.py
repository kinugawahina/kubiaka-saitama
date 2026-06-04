import json
import folium

with open("data/processed/sightings_2018_2024.geojson", "r", encoding="utf-8") as f:
    sightings = json.load(f)

m = folium.Map(
    location=[35.95, 139.45],
    zoom_start=10,
    tiles="OpenStreetMap",
)

colors = {
    "2018": "blue",
    "2019": "green",
    "2020": "purple",
    "2021": "orange",
    "2022": "red",
    "2023": "darkred",
    "2024": "black",
}

for year, color in colors.items():
    year_features = {
        "type": "FeatureCollection",
        "features": [
            f for f in sightings["features"]
            if str(f["properties"].get("year")) == year
        ],
    }

    folium.GeoJson(
        year_features,
        name=f"発生確認地点 {year}年度",
        marker=folium.CircleMarker(
            radius=4,
            color=color,
            fill=True,
            fill_opacity=0.7,
        ),
        tooltip=folium.GeoJsonTooltip(
            fields=["year"],
            aliases=["年度"],
        ),
    ).add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

m.save("maps/kubiaka_map.html")
print("created: maps/kubiaka_map.html")