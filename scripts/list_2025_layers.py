import json

ITEM_ID = "025e1975b68248f3b6cb201254df9815"

with open(f"data/raw/2025_{ITEM_ID}_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def walk_layers(layers, prefix=""):
    for i, layer in enumerate(layers):
        path = f"{prefix}{i}"
        print("=" * 80)
        print("path:", path)
        print("title:", layer.get("title"))
        print("layerType:", layer.get("layerType"))
        print("url:", layer.get("url"))
        print("itemId:", layer.get("itemId"))

        sublayers = layer.get("layers") or layer.get("featureCollection", {}).get("layers") or []
        if sublayers:
            walk_layers(sublayers, prefix=f"{path}.")

walk_layers(data.get("operationalLayers", []))