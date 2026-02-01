import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"

params = {
    "ServiceKey": os.getenv("KMA_SERVICE_KEY"),
    "dataType": "JSON",
    "dataCd": "ASOS",
    "dateCd": "DAY",
    "startDt": "20250101",
    "endDt": "20251231",
    "stnIds": "108",   # 서울
    "numOfRows": 999,
    "pageNo": 1
}

items = []
while True:
    res = requests.get(URL, params=params, timeout=30)
    res.raise_for_status()
    body = res.json()["response"]["body"]

    page_items = body.get("items", {}).get("item", [])
    if not page_items:
        break

    if isinstance(page_items, dict):
        page_items = [page_items]

    items.extend(page_items)

    if len(items) >= int(body["totalCount"]):
        break

    params["pageNo"] += 1

df = pd.DataFrame(items)
out = "data/raw/weather/asos_daily_2025_preview.csv"
os.makedirs("data/raw/weather", exist_ok=True)
df.to_csv(out, index=False, encoding="utf-8-sig")

print("saved:", out)
print("rows:", len(df))
print(df.head())
