from pathlib import Path
import pandas as pd

RAW = Path("data/raw/weather/asos_daily_2025_preview.csv")
OUT = Path("data/processed/weather_daily.csv")

def main():
    df = pd.read_csv(RAW)

    # 필요한 컬럼만 (ASOS 원본 컬럼명 기준)
    use = {
        "tm": "date",
        "avgTa": "avg_temp",
        "minTa": "min_temp",
        "maxTa": "max_temp",
        "sumRn": "precip_mm",
    }

    keep = [c for c in use.keys() if c in df.columns]
    out = df[keep].rename(columns=use)

    # 타입 정리
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    for c in ["avg_temp", "min_temp", "max_temp", "precip_mm"]:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")

    # 최소 QA: 날짜 없는 행 제거, 날짜 정렬
    out = out.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)

    # precip_mm는 0(비 안 옴)과 NaN(관측 누락)을 구분해야 하므로 NaN은 그대로 둠
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)

    print(f"saved: {OUT} ({len(out)} rows)")
    print(out.head())

if __name__ == "__main__":
    main()
