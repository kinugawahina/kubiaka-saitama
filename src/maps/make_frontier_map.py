import json
import folium
import numpy as np
from sklearn.neighbors import BallTree

INPUT = "data/processed/sightings_2018_2024.geojson"
OUTPUT = "maps/kubiaka_frontier_2018_2024.html"

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

features = data["features"]

f2018 = [f for f in features if f["properties"].get("year") == "2018"]
f2024 = [f for f in features if f["properties"].get("year") == "2024"]

coords2018 = np.array([
    [f["geometry"]["coordinates"][1], f["geometry"]["coordinates"][0]]
    for f in f2018
])

tree = BallTree(np.radians(coords2018), metric="haversine")

frontier = []

for f in f2024:
    lon, lat = f["geometry"]["coordinates"]
    dist, idx = tree.query(np.radians([[lat, lon]]), k=1)
    km = float(dist[0][0] * 6371)
    nearest_2018 = f2018[int(idx[0][0])]

    p = f["properties"]
    p["frontier_distance_km"] = km
    p["nearest_2018_coordinates"] = nearest_2018["geometry"]["coordinates"]

    # 公開版では個人宅を除外
    if p.get("施設区分") == "個人宅":
        continue

    frontier.append(f)

frontier = sorted(
    frontier,
    key=lambda x: x["properties"].get("frontier_distance_km", 0),
    reverse=True,
)

top_frontier = frontier[:150]

m = folium.Map(
    location=[36.0, 139.45],
    zoom_start=9,
    tiles="OpenStreetMap",
)

# 2018 コア地点
for f in f2018:
    lon, lat = f["geometry"]["coordinates"]
    p = f["properties"]

    folium.CircleMarker(
        location=[lat, lon],
        radius=3,
        color="gray",
        fill=True,
        fill_opacity=0.45,
        tooltip="2018 コア地点",
        popup=folium.Popup(
            f"""
            <b>2018地点</b><br>
            市町村: {p.get("city_norm") or ""}<br>
            施設: {p.get("施設名称") or ""}<br>
            """,
            max_width=320,
        ),
    ).add_to(m)

# 2024 前線候補
for rank, f in enumerate(top_frontier, start=1):
    lon, lat = f["geometry"]["coordinates"]
    p = f["properties"]

    city = p.get("city_norm") or ""
    facility = p.get("施設名称") or ""
    facility_type = p.get("施設区分") or ""
    tree_name = p.get("tree_norm") or ""
    adults = p.get("adult_count_norm") or 0
    distance = p.get("frontier_distance_km") or 0

    radius = min(16, max(6, distance / 2))

    popup = f"""
    <b>前線候補 #{rank}</b><br>
    市町村: {city}<br>
    施設区分: {facility_type}<br>
    施設: {facility}<br>
    樹種: {tree_name}<br>
    成虫頭数: {adults}<br>
    2018地点からの最近傍距離: {distance:.2f} km
    """

    nearest_lon, nearest_lat = p["nearest_2018_coordinates"]

    folium.PolyLine(
        locations=[
            [nearest_lat, nearest_lon],
            [lat, lon],
        ],
        color="blue",
        weight=2,
        opacity=0.35,
        tooltip=f"2018地点から {distance:.1f} km",
    ).add_to(m)

    folium.CircleMarker(
        location=[lat, lon],
        radius=radius,
        color="blue",
        fill=True,
        fill_opacity=0.75,
        tooltip=f"#{rank} {city} / {distance:.1f}km",
        popup=folium.Popup(popup, max_width=420),
    ).add_to(m)

folium.LayerControl().add_to(m)

legend_html = """
<div style="
position: fixed;
bottom: 30px;
left: 30px;
z-index: 9999;
background: white;
padding: 12px;
border: 1px solid #aaa;
border-radius: 8px;
font-size: 14px;
line-height: 1.6;
">
<b>拡散前線マップ</b><br>
<span style="color: gray;">●</span> 2018年の初期確認地点<br>
<span style="color: blue;">●</span> 2024年の前線候補<br>
<span style="color: blue;">━</span> 直前年までの最寄り確認地点との距離<br>
<br>
各年度の地点について、それ以前の年度に確認された地点から
どれだけ離れているかを計算しています。<br>
距離が大きい地点は、その年に既知分布の外側で確認された
拡散前線候補です。
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

m.save(OUTPUT)

print("2018 core points:", len(f2018))
print("frontier candidates:", len(top_frontier))
print("created:", OUTPUT)

print("\nTop 20 frontier candidates:")
for rank, f in enumerate(top_frontier[:20], start=1):
    p = f["properties"]
    print(
        rank,
        round(p["frontier_distance_km"], 2),
        p.get("city_norm"),
        p.get("施設名称"),
        p.get("adult_count_norm") or 0,
    )