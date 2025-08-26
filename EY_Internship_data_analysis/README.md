# Shoe Sales Data Cleaning & Descriptive Analysis

## Overview
This project focuses on **data cleaning, standardization, and descriptive analytics** for a global shoe sales dataset.  
The workflow consists of two major stages:

1. **Data Cleaning & Standardization (`basic_cleaning.py`)**  
   - Merges multiple raw data sources (shoe facts, shoe dimensions, country information, forex data).  
   - Standardizes prices to **Euros (€)** using historical exchange rates.  
   - Harmonizes shoe sizes across **US, UK, and EU metrics** for men, women, and kids.  
   - Produces a **final cleaned dataset** for downstream analysis.  

2. **Descriptive Analysis & Visualization (`descriptive_analysis.py`)**  
   - Conducts exploratory and statistical analyses to uncover insights into availability, sales, demographics, and pricing.  
   - Visualizes results through clear and interpretable charts.  

---

## Data Sources
- **`shoes_fact.csv`** → transactional/availability data per shoe ID.  
- **`shoes_dim.csv`** → metadata (name, gender, etc.) about each shoe.  
- **`country_dim.csv`** → country codes, currencies, and metrics.  
- **`daily_forex_rates.csv`** → historical exchange rates (base currency = EUR).  

---

## Methods

### 1. Data Cleaning (`basic_cleaning.py`)
- **Merging datasets** by `country_code` and `id`.  
- **Date handling** with consistent parsing.  
- **Currency standardization** → converting all prices to Euros (€) using forex rates.  
- **Shoe size conversion** → mapping US/UK sizes to standardized EU sizing across genders and kids’ models.  
- **Data sampling & plotting** → availability trends over time for a random sample of shoes.  
- **Final export**: A clean dataset `final_shoes_merged.csv` ready for analysis.  

### 2. Descriptive Analysis (`descriptive_analysis.py`)
Analysis covers three main themes:

#### A. By Shoe Model
- **Q1:** Top 5 models by total availability.  
- **Q2:** Bottom 5 models by non-zero availability (excluding deadstock).  
- **Q3:** Models with highest sales (net availability decrease).  
- **Q4:** Deadstock models (no change in availability).  

#### B. By Demographics & Geography
- **Q5:** Sell-out rates by gender.  
- **Q6:** Countries with the highest total sales.  
- **Q7:** Cross-country sales volume by price segment.  

#### C. Other Analyses
- **Q8:** Correlation between average price and total sales volume.  
- **Q9:** Price differences between deadstock vs. active models.  

---

## Visualizations
The analysis produces a **pdf of plots**, covering all nine key questions. Examples include:

- Horizontal bar charts for **top/bottom shoe models**.  
- Comparative bar plots for **deadstock vs. active models**.  
- Gender-based **sell-out rate charts**.  
- Country-level sales distributions by **price segment**.  
- Scatter plots with regression lines for **price vs. sales correlation**.  
- Boxplots comparing **deadstock vs. active price distributions**.  

---

## Results (Highlights)
- Some models had consistently high availability, while others showed **deadstock behavior** (no movement).  
- Sell-out rates varied across **gender demographics**, with notable differences in demand.  
- Countries showed **heterogeneous sales patterns**, strongly tied to price segments.  
- A measurable **negative correlation** was found between shoe price and sales volume (higher-priced shoes tended to sell less and remain deadstock longer).  

---

## Acknowledgements
This project was completed as part of an internship in data analytics at EY.  
Special thanks to the **Arnik Khillar** and the **EY Data Team** for guiding me and providing the datasets.  
