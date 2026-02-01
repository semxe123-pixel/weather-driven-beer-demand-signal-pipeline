-- 기온 구간별 평균 검색량
SELECT
    CASE
        WHEN avg_temp < 0 THEN '<0'
        WHEN avg_temp < 10 THEN '0-10'
        WHEN avg_temp < 20 THEN '10-20'
        WHEN avg_temp < 25 THEN '20-25'
        WHEN avg_temp < 30 THEN '25-30'
        ELSE '30+'
    END AS temp_bin,
    AVG(beer_search_index) AS avg_beer_search
FROM beer_signal.demand_signal_daily_clean
GROUP BY temp_bin
ORDER BY FIELD(temp_bin, '<0','0-10','10-20','20-25','25-30','30+');