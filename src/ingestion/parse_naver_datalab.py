from pathlib import Path
import pandas as pd

RAW = Path("data/raw/search_trend/naver_datalab_raw.xlsx")
OUT = Path("data/processed/search_interest_daily.csv")

def parse():
    df = pd.read_excel(RAW, sheet_name="개요", header=None)

    # 헤더(날짜가 시작되는 행) 찾기
    hdr = df.index[df.iloc[:, 0].astype(str).str.contains("날짜", na=False)][0]

    data = df.iloc[hdr:].copy()
    data.columns = data.iloc[0]
    data = data.iloc[1:, :4].copy()
    data.columns = ["date_beer", "beer", "date_hangang", "hangang"]

    out = pd.DataFrame({
        "date": pd.to_datetime(data["date_beer"], errors="coerce"),
        "beer_search_index": pd.to_numeric(data["beer"], errors="coerce"),
        "hangang_search_index": pd.to_numeric(data["hangang"], errors="coerce"),
    }).dropna(subset=["date"]).sort_values("date")

    # search index는 0~100 범위 밖이면 결측 처리
    for c in ["beer_search_index", "hangang_search_index"]:
        out.loc[~out[c].between(0, 100), c] = pd.NA

    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)

    print(f"saved: {OUT} ({len(out)} rows)")

if __name__ == "__main__":
    parse()
