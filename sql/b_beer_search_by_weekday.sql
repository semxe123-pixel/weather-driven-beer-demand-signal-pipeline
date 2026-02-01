-- 요일별 평균 검색량
SELECT
    weekday,
    AVG(beer_search_index) AS avg_beer_search
FROM beer_signal.demand_signal_daily_clean
GROUP BY weekday
ORDER BY FIELD(weekday, 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');
