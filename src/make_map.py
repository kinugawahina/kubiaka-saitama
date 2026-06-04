import folium

m = folium.Map(
    location=[35.95, 139.45],
    zoom_start=10,
)

# 仮の候補地点：川島町役場周辺
folium.Marker(
    location=[35.9815, 139.4818],
    popup="川島町 周辺",
    tooltip="調査候補",
).add_to(m)

m.save("maps/kubiaka_map.html")

print("created: maps/kubiaka_map.html")