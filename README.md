# 🍺 Weather-Driven Beer Demand Signal Pipeline

![Python](https://img.shields.io/badge/Python-3.9-blue?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-ETL-150458?style=flat-square&logo=pandas&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Data%20Mart-003B57?style=flat-square&logo=mysql&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Modular-success?style=flat-square)
![Status](https://img.shields.io/badge/Status-Completed-gray?style=flat-square)

> **A modular ETL pipeline designed to detect beer demand signals by correlating Weather Data (KMA API) with Search Volume Data (Naver DataLab).**
---

## 📌 1. Project Overview

In the absence of actual sales data, this project defines **"Search Volume" as a proxy for potential demand** to quantify how temperature changes impact consumer interest in beer.

The primary goal is to build a **robust and modular data pipeline** where each stage—Ingestion, Transformation, and Load—is **decoupled** into independent scripts. This architecture ensures better maintainability and prepares the system for future orchestration (e.g., Airflow).

### 🧐 Background & Motivation
* **Weather Sensitivity:** Beer consumption is highly sensitive to weather conditions. I aimed to identify specific **temperature thresholds** to provide data-driven insights.
* **Engineering Focus (Modularity):** Instead of a monolithic script, I focused on **Separation of Concerns**. By isolating the Ingestion, QA, and Transformation logic, I built a system that is easy to debug and scalable for future automation tools.

### 🎯 Key Objectives
1.  **Modular Pipeline Design:** Designed the pipeline as **independent modules** (Ingestion → QA → Transform → Mart) to ensure clear logic separation and reusability.
2.  **Hybrid Data Ingestion:** Seamless integration of **Dynamic Data** (KMA Weather API) and **Static Data** (Naver DataLab Excel/CSV).
3.  **Systematic Data QA:** Implemented strict validation logic (Null checks, Type enforcement) within the pipeline to filter out "Garbage Data" before the loading process.
4.  **SQL Data Mart:** Designed a structured Data Mart optimized for analytical queries (OLAP) to derive business intelligence.

### 🚀 Future Roadmap
* **Orchestration:** Plan to integrate **Apache Airflow** to schedule and manage the dependencies of these decoupled scripts.

---

## 🏗 2. System Architecture

This project is designed as a simple yet expandable **batch-style data pipeline**.
Rather than focusing on automation tools, the architecture emphasizes
**clear separation of responsibilities across data stages**.

### Overall Flow

```text
External Data Sources
 ├─ Naver DataLab (Excel)
 └─ KMA ASOS Open API (JSON)
          ↓
Ingestion Layer (Python)
 ├─ parse_naver_datalab.py
 └─ asos_preview_2025.py
          ↓
Processed Layer
 ├─ search_interest_daily.csv
 └─ weather_daily.csv
          ↓
Transformation / Mart Creation
 └─ demand_signal_daily.csv
          ↓
MySQL
 └─ demand_signal_daily table
          ↓
SQL Aggregation & Analysis
 └─ a/b/c analysis queries
          ↓
Visualization & Reporting
 └─ figures (charts & insights)
```
---

## 🛠 3. Key Engineering Features

### 1. Layered Data Architecture (Raw → Processed → Mart)
Instead of directly analyzing raw external data, the pipeline is designed with
clearly separated layers: Raw, Processed, and Mart.
Weather API data and search trend data are first cleaned and standardized in the
Processed layer before being used to generate the Daily Demand Signal Mart,
ensuring data consistency and reproducibility.

### 2. Master Mart–Centered Analysis Structure
All SQL analyses are based on a single master table, `demand_signal_daily`.
Aggregated results such as temperature-bin analysis, weekday patterns,
and weekend effects are stored as separate result marts.
This approach treats SQL outputs as reusable data assets rather than
one-off query results.

### 3. Clear Separation Between SQL Logic and Analysis Outputs
Aggregation and analysis logic are implemented in SQL,
and query results are exported as CSV files for visualization and reporting.
This separation makes the data transformation process transparent
and allows analysis results to be easily traced back to their source queries.

### 4. Batch-Oriented ETL Pipeline Design
The ETL pipeline is implemented as a batch-oriented script that,
when executed, performs the entire process from raw data ingestion
to mart generation in a single run.
The structure is designed to be easily extendable to scheduled execution
using a workflow scheduler in the future.

---

## 📊 4. Analysis Results & Insights

This section summarizes key insights derived from the Demand Signal Mart
and demonstrates how weather-related features influence beer demand signals.

### 4.1 Overall Relationship Between Temperature and Beer Demand
<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/5742d756-eea3-4892-8ab0-2ef601703166" />

Daily average temperature shows a clear seasonal pattern that aligns
with beer-related search interest.
Higher temperatures generally correspond to higher search volumes,
supporting the assumption that temperature is a primary demand driver.

- Input: `demand_signal_daily`
- Method: Time-series comparison (temperature vs search index)

### 4.2 Demand Differences by Temperature Range
<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/d3f4609e-3c66-42ef-a3e1-025562492ffb" />

When temperature is grouped into predefined bins,
beer search interest increases as temperature rises,
with the highest demand observed in the 30°C+ range.

- Output Mart: `beer_search_by_temp_bin`
- Insight: Demand response is non-linear and accelerates at higher temperatures

### 4.3 Weekday vs Weekend Demand Pattern
<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/a1a2bc0e-e5d6-47ac-b385-e15ab009b8f2" />

Beer-related search interest is consistently higher on weekends,
with a noticeable uplift on Fridays and Saturdays.

- Output Mart: `beer_search_by_weekday`
- Insight: Temporal factors (weekday/weekend) significantly affect demand behavior

### 4.4 Interaction Effect Between Temperature and Weekend
<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/56fe4cc7-cd6a-4d17-a165-05f2286ded39" />

Weekend uplift becomes more pronounced at higher temperature ranges.
At the same temperature level, weekends show higher demand signals
than weekdays.

- Output Mart: `beer_search_temp_weekend_effect`
- Insight: Temperature and weekend effects interact rather than act independently

### 4.5 Short-Term Demand Sensitivity to Temperature Change
<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/93d38b02-ee73-4f2d-8291-35b99f3dc25b" />

Day-over-day temperature changes show a weak but positive relationship
with percentage changes in beer search interest.
This suggests that sudden temperature increases can trigger
short-term demand responses.

- Method: Delta temperature vs delta search analysis
- Insight: Temperature change acts as a short-term demand accelerator

---

## 🚀 5. How to Run

This project is implemented as a batch-style ETL pipeline.
By running each script in order, data ingestion, transformation, and analysis
are performed end-to-end.

---

### 1️⃣ Environment Setup

```bash
# Clone repository
git clone https://github.com/semxe123-pixel/weather-driven-beer-demand-signal-pipeline.git
cd weather-driven-beer-demand-signal-pipeline

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Data Ingestion

#### (1) Naver DataLab Search Data

- Download search trend data manually from **Naver DataLab**
- Place the Excel file under the following directory:

```text
data/raw/search_trend/
```
- Parse and normalize the raw Excel data:

```bash
python src/ingestion/parse_naver_datalab.py
```

#### (2) ASOS Daily Weather Data (API)

- Fetch daily weather data from the ASOS Open API:

```bash
python src/ingestion/asos_preview_2025.py
```

- Raw weather data will be stored under:

```text
data/raw/weather/
```

### 3️⃣ Data Transformation

- Clean, validate, and standardize daily-level weather data:

```bash
python src/transformation/build_weather_daily.py
```
- Processed datasets will be generated under:

```text
data/processed/
```

### 4️⃣ Demand Signal Mart Creation
- Join weather data and search interest data to build the demand signal mart:

```bash
python src/transformation/build_demand_signal_mart.py
```
- Output mart table:

```text
data/mart/demand_signal_daily.csv
```

### 5️⃣ Analysis & Visualization

- Generate analysis results and visualizations from the mart table:

```bash
python src/analysis/make_figures.py
```

- Figures will be saved under:

```text
reports/figures/
```
---
