import json
from datetime import datetime, timezone, timedelta

import folium

SIGHTINGS_2024 = "data/processed/sightings_2018_2024.geojson"
REPORTS_2025 = "data/processed/reports_2025.geojson"
OUTPUT = "maps/kubiaka_latest_2024_2025.html"

JST = timezone(timedelta(hours=9))

with open(SIGHTINGS_2024, encoding="utf-8") as f:
    all_sightings = json.load(f)

with open(REPORTS_2025, encoding="utf-8") as f:
    reports_2025 = json.load(f)

sightings_2024 = [
    f for f in all_sightings["features"]
    if f["properties"].get("year") == "2024"
]

m = folium.Map(
    location=[36.0, 139.45],
    zoom_start=9,
    tiles="OpenStreetMap",
)

# 2024行政確認地点
for f in sightings_2024:
    p = f["properties"]
    lon, lat = f["geometry"]["coordinates"]

    city = p.get("city_norm") or ""
    facility = p.get("施設名称") or ""
    address = p.get("住所") or p.get("詳細住所等") or ""
    adults = p.get("adult_count_norm") or 0
    tree = p.get("tree_norm") or ""

    popup = f"""
    <b>2024行政確認</b><br>
    市町村: {city}<br>
    施設: {facility}<br>
    住所: {address}<br>
    樹種: {tree}<br>
    成虫頭数: {adults}
    """

    folium.CircleMarker(
        location=[lat, lon],
        radius=3,
        color="red",
        fill=True,
        fill_opacity=0.45,
        popup=folium.Popup(popup, max_width=380),
    ).add_to(m)

# 2025市民報告地点
for f in reports_2025["features"]:
    p = f["properties"]
    lon, lat = f["geometry"]["coordinates"]

    day = p.get("day")
    if day:
        try:
            date = datetime.fromtimestamp(day / 1000, JST).strftime("%Y-%m-%d")
        except Exception:
            date = ""
    else:
        date = ""

    tree = p.get("tree") or ""
    status = p.get("hasei") or ""
    content = p.get("naiyo") or ""
    hon = p.get("hon") or ""
    hiki = p.get("hiki") or ""
    place = p.get("field_13") or ""

    popup = f"""
    <b>2025市民報告</b><br>
    日付: {date}<br>
    樹種: {tree}<br>
    状況: {status}<br>
    内容: {content}<br>
    本数: {hon}<br>
    匹数: {hiki}<br>
    場所: {place}
    """

    folium.CircleMarker(
        location=[lat, lon],
        radius=8,
        color="blue",
        fill=True,
        fill_opacity=0.8,
        tooltip=f"2025報告 / {content}",
        popup=folium.Popup(popup, max_width=420),
    ).add_to(m)

m.save(OUTPUT)

print("2024 sightings:", len(sightings_2024))
print("2025 reports:", len(reports_2025["features"]))
print(f"created: {OUTPUT}")