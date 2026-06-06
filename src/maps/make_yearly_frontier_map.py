import json
import folium
import numpy as np
from sklearn.neighbors import BallTree

INPUT = "data/processed/sightings_2018_2024.geojson"
OUTPUT = "maps/kubiaka_yearly_frontier.html"

YEAR_COLORS = {
    "2019": "blue",
    "2020": "green",
    "2021": "orange",
    "2022": "red",
    "2023": "purple",
    "2024": "black",
}

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

features = data["features"]

m = folium.Map(
    location=[36.0, 139.45],
    zoom_start=9,
    tiles="OpenStreetMap",
)

all_previous = []

for year in ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]:

    current = [
        f for f in features
        if f["properties"].get("year") == year
    ]

    if year == "2018":
        all_previous.extend(current)

        for f in current:
            lon, lat = f["geometry"]["coordinates"]

            folium.CircleMarker(
                location=[lat, lon],
                radius=2,
                color="gray",
                fill=True,
                fill_opacity=0.4,
                tooltip="2018 初期確認地点",
            ).add_to(m)

        continue

    previous_coords = np.array([
        [
            f["geometry"]["coordinates"][1],
            f["geometry"]["coordinates"][0],
        ]
        for f in all_previous
    ])

    tree = BallTree(
        np.radians(previous_coords),
        metric="haversine"
    )

    candidates = []

    for f in current:

        lon, lat = f["geometry"]["coordinates"]

        dist, idx = tree.query(
            np.radians([[lat, lon]]),
            k=1
        )

        km = float(dist[0][0] * 6371)

        nearest = all_previous[int(idx[0][0])]

        candidates.append(
            (
                km,
                f,
                nearest
            )
        )

    candidates.sort(reverse=True, key=lambda x: x[0])

    # 各年上位30地点だけ表示
    top = candidates[:30]

    color = YEAR_COLORS[year]

    for km, current_f, nearest_f in top:

        p = current_f["properties"]

        if p.get("施設区分") == "個人宅":
            continue

        lon, lat = current_f["geometry"]["coordinates"]

        nearest_lon, nearest_lat = (
            nearest_f["geometry"]["coordinates"]
        )

        city = p.get("city_norm") or ""
        facility = p.get("施設名称") or ""

        folium.PolyLine(
            [
                [nearest_lat, nearest_lon],
                [lat, lon],
            ],
            color=color,
            weight=2,
            opacity=0.35,
        ).add_to(m)

        folium.CircleMarker(
            location=[lat, lon],
            radius=min(14, max(6, km / 2)),
            color=color,
            fill=True,
            fill_opacity=0.8,
            tooltip=f"{year} / {city} / {km:.1f}km",
            popup=f"""
            <b>{year}年度 前線候補</b><br>
            市町村: {city}<br>
            施設: {facility}<br>
            既知地点からの距離: {km:.2f} km
            """,
        ).add_to(m)

    all_previous.extend(current)

legend = """
<div style="
position: fixed;
bottom: 30px;
left: 30px;
z-index: 9999;
background: white;
padding: 12px;
border: 1px solid #aaa;
border-radius: 8px;
font-size: 13px;
line-height: 1.5;
max-width: 320px;
">
<b>年度別拡散前線マップ</b><br><br>

灰色：2018年度確認地点<br>

青：2019前線候補<br>
緑：2020前線候補<br>
橙：2021前線候補<br>
赤：2022前線候補<br>
紫：2023前線候補<br>
黒：2024前線候補<br><br>

各年度について、それ以前に確認されていた地点から
最も離れていた地点群を表示しています。
</div>
"""

m.get_root().html.add_child(
    folium.Element(legend)
)

m.save(OUTPUT)

print("created:", OUTPUT)