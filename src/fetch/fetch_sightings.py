import json
import requests

LAYERS = {
    "2018": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/クビアカ確認情報2018年度/FeatureServer/0",
    "2019": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/クビアカ確認情報2019年度/FeatureServer/0",
    "2020": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/クビアカ確認情報2020年度/FeatureServer/0",
    "2021": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/クビアカ確認情報2021年度/FeatureServer/0",
    "2022": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/クビアカ確認情報2022年度/FeatureServer/0",
    "2023": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/クビアカ確認情報2023年度/FeatureServer/0",
    "2024": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/クビアカ2024発生確認/FeatureServer/0",
}

features = []

for year, url in LAYERS.items():
    print(f"fetching {year}...")

    r = requests.get(
        f"{url}/query",
        params={
            "f": "geojson",
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "true",
        },
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()

    for feature in data.get("features", []):
        props = feature.setdefault("properties", {})

        props["year"] = year
        props["source_layer"] = url

        # 年度ごとに違うフィールド名を共通化
        props["city_norm"] = props.get("市町村名") or props.get("市町村")
        props["tree_norm"] = props.get("樹種") or props.get("被害樹種")
        props["adult_count_norm"] = props.get("確認_成虫") or props.get("成虫頭数")
        props["larva_count_norm"] = props.get("確認_幼虫") or props.get("幼虫頭数")
        props["frass_norm"] = props.get("確認_フラス") or props.get("フラス確認")
        props["date_found_norm"] = props.get("発見年月日") or props.get("県確知日")

        features.append(feature)

out = {
    "type": "FeatureCollection",
    "features": features,
}

with open("data/processed/sightings_2018_2024.geojson", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"saved {len(features)} features")
print("data/processed/sightings_2018_2024.geojson")