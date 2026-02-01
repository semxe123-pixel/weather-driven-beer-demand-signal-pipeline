# Weather-Driven Beer Demand Signal Pipeline

## Overview
This project explores how weather conditions influence beer demand signals,
using search interest data as a proxy for real-world consumption.

Due to limited access to actual sales data, this project leverages
Naver DataLab search trends ("맥주", "한강") combined with
Korea Meteorological Administration (ASOS) daily weather data.

## Data Sources
- Naver DataLab search trend data (Excel)
- KMA ASOS daily weather data (Open API)

## Pipeline Structure
1. Data ingestion from external sources (Excel, API)
2. Data validation and preprocessing (Python)
3. Demand signal mart creation
4. SQL-based aggregation and analysis
5. Visualization and insight generation

## Tech Stack
- Python (pandas, requests)
- MySQL
- SQL (aggregation & analysis)
- Git / GitHub

## Key Analyses
- Beer search interest by temperature bins
- Weekday vs weekend demand patterns
- Interaction effect between temperature and weekend
- Correlation between temperature change and demand change

## Outcome
The analysis confirms a strong positive relationship between rising temperature
and beer-related search interest, with a consistent weekend uplift effect,
especially in higher temperature ranges.

