import json
import re

with open("data/raw/dashboard_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

text = json.dumps(data, ensure_ascii=False)

# ArcGIS itemId は32文字の16進文字列
ids = sorted(set(re.findall(r"\b[a-f0-9]{32}\b", text)))

print(f"candidate itemIds: {len(ids)}")
for item_id in ids:
    print(item_id)