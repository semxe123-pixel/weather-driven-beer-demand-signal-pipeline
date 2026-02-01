-- 같은 기온대에서도 주말 효과 검증
SELECT
    temp_bin,
    is_weekend,
    AVG(beer_search_index) AS avg_beer_search
FROM (
    SELECT
    *,
    CASE
        WHEN avg_temp < 20 THEN '<20'
        WHEN avg_temp < 25 THEN '20-25'
        WHEN avg_temp < 30 THEN '25-30'
        ELSE '30+'
    END AS temp_bin
    FROM beer_signal.demand_signal_daily_clean
) t
GROUP BY temp_bin, is_weekend
ORDER BY FIELD(temp_bin, '<20','20-25','25-30','30+'), is_weekend;
