from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

MART = Path("data/mart/demand_signal_daily.csv")
OUT = Path("reports/figures")

def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)

def main():
    OUT.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(MART, parse_dates=["date"]).sort_values("date")
    if "avg_temp" not in df.columns or "beer_search_index" not in df.columns:
        raise ValueError("mart columns missing. expected avg_temp, beer_search_index, date")

    # 1) 일평균 기온 vs 맥주 검색량 (dual axis)
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    l1, = ax1.plot(
        df["date"],
        df["avg_temp"],
        color="tab:red",
        label="Avg Temp (C)"
    )

    l2, = ax2.plot(
        df["date"],
        df["beer_search_index"],
        color="tab:blue",
        label="Beer Search Index"
    )

    ax1.set_title("Avg Temp vs Beer Search")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Avg Temp (C)", color="tab:red")
    ax2.set_ylabel("Beer Search Index", color="tab:blue")

    # y축 색도 선 색이랑 맞춤
    ax1.tick_params(axis="y", labelcolor="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:blue")

    # 범례 하나로 합치기
    ax1.legend(handles=[l1, l2], loc="upper left")

    save(fig, "fig1_temp_vs_beer.png")

    # 2) 기온 구간별 평균 검색량
    bins = [-50, 0, 10, 20, 25, 30, 100]
    labels = ["<0", "0-10", "10-20", "20-25", "25-30", "30+"]
    t = df.copy()
    t["temp_bin"] = pd.cut(t["avg_temp"], bins=bins, labels=labels, right=False)
    g = t.groupby("temp_bin", observed=True)["beer_search_index"].mean()

    fig, ax = plt.subplots()
    ax.bar(g.index.astype(str), g.values)
    ax.set_title("Beer Search by Temp Bin")
    ax.set_xlabel("Temp Bin (C)")
    ax.set_ylabel("Mean Search Index")
    save(fig, "fig2_temp_bins.png")

    # 3) 요일별 평균 검색량
    w = df.copy()
    w["weekday"] = w["date"].dt.weekday  # 0=Mon
    order = [0, 1, 2, 3, 4, 5, 6]
    names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    g = w.groupby("weekday")["beer_search_index"].mean().reindex(order)

    fig, ax = plt.subplots()
    ax.bar(names, g.values)
    ax.set_title("Beer Search by Weekday")
    ax.set_xlabel("Weekday")
    ax.set_ylabel("Mean Search Index")
    save(fig, "fig3_weekday.png")

    # 4) 한강 검색량 vs 기온 (scatter)
    if "hangang_search_index" in df.columns:
        fig, ax = plt.subplots()
        ax.scatter(
            df["avg_temp"],
            df["hangang_search_index"],
            alpha=0.35,
            s=18,
            linewidths=0,
        )
        ax.set_title("Hangang Search vs Avg Temp")
        ax.set_xlabel("Avg Temp (C)")
        ax.set_ylabel("Hangang Search Index")
        save(fig, "fig4_hangang_vs_temp.png")

    # 5) 기온 변화량 vs 검색량 변화율 (scatter + simple fit line)
    d = df[["date", "avg_temp", "beer_search_index"]].copy()
    d["d_temp"] = d["avg_temp"].diff()
    d["d_beer_pct"] = d["beer_search_index"].pct_change() * 100
    d = d.dropna()

    fig, ax = plt.subplots()
    ax.scatter(d["d_temp"], d["d_beer_pct"], alpha=0.4, s=18, linewidths=0)

    # 회귀선(1차) - 관계 방향만 보여주기
    m, b = d[["d_temp", "d_beer_pct"]].dropna().pipe(
        lambda x: (x["d_temp"].to_numpy(), x["d_beer_pct"].to_numpy())
    )
    # numpy 없이도 되는 방식으로
    coef = pd.Series(d["d_temp"]).cov(d["d_beer_pct"]) / pd.Series(d["d_temp"]).var()
    intercept = d["d_beer_pct"].mean() - coef * d["d_temp"].mean()

    x0, x1 = d["d_temp"].min(), d["d_temp"].max()
    ax.plot([x0, x1], [coef * x0 + intercept, coef * x1 + intercept])

    ax.set_title("Delta Temp vs Beer Search % Change")
    ax.set_xlabel("Delta Avg Temp (C)")
    ax.set_ylabel("Beer Search % Change")
    save(fig, "fig5_delta_temp_vs_delta_search.png")

if __name__ == "__main__":
    main()
