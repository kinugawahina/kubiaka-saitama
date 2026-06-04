import json

ITEM_ID = "2f4e26251a324bb080c31a827934c3d1"

with open(f"data/raw/{ITEM_ID}_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

layers = data.get("operationalLayers", [])

print(f"layers: {len(layers)}")

for i, layer in enumerate(layers):
    print("=" * 60)
    print("index:", i)
    print("title:", layer.get("title"))
    print("layerType:", layer.get("layerType"))
    print("url:", layer.get("url"))
    print("itemId:", layer.get("itemId"))