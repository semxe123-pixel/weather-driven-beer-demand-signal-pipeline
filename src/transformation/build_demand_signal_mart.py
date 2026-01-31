from pathlib import Path
import pandas as pd

SEARCH = Path("data/processed/search_interest_daily.csv")
WEATHER = Path("data/processed/weather_daily.csv")
OUT = Path("data/mart/demand_signal_daily.csv")

def main():
    s = pd.read_csv(SEARCH, parse_dates=["date"])
    w = pd.read_csv(WEATHER, parse_dates=["date"])

    # 날짜 단위 보장(혹시 모를 중복 대비)
    s = s.drop_duplicates(subset=["date"]).sort_values("date")
    w = w.drop_duplicates(subset=["date"]).sort_values("date")

    # 기본은 inner join: 둘 다 있는 날짜만 남김
    df = s.merge(w, on="date", how="inner")

    # 실무 느낌 옵션: 요일, 주말 플래그
    df["weekday"] = df["date"].dt.day_name()   # 영어 요일
    df["is_weekend"] = df["date"].dt.weekday >= 5

    # (선택) 폭염 플래그: 최고기온 33도 이상
    if "max_temp" in df.columns:
        df["heatwave_flag"] = df["max_temp"] >= 33

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)

    print(f"saved: {OUT} ({len(df)} rows)")
    print(df.head())

if __name__ == "__main__":
    main()
