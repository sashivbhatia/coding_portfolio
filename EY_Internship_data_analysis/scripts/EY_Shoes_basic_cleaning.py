from forex_python.converter import CurrencyRates
from forex_python.converter import RatesNotAvailableError
import pandas as pd
from datetime import datetime
from tqdm import tqdm
tqdm.pandas()
import matplotlib.pyplot as plt
import random

# Load files (all now inside the GitHub repo /data folder)
base_path = "C:/UW/Github/coding_portfolio/EY_Internship_data_analysis/data/"

shoes_fact = pd.read_csv(base_path + "shoes_fact.csv")
shoes_dim = pd.read_csv(base_path + "shoes_dim.csv")
country_dim = pd.read_csv(base_path + "country_dim.csv")
forex_df = pd.read_csv(base_path + "daily_forex_rates.csv")

# Merge files by Country Code and ID
shoes_merged = shoes_fact.merge(
    country_dim[['country_code', 'currency', 'shoe_metric']], 
    on='country_code', how='left'
)
shoes_merged = shoes_merged.merge(
    shoes_dim[['id', 'gender']], left_on='id', right_on='id', how='left'
)
shoes_merged['date'] = pd.to_datetime(shoes_merged['date'], dayfirst=True, errors='coerce')
print(shoes_merged.head())

currency_map = {
    'euro': 'EUR',
    'usd': 'USD',
    'pounds': 'GBP'
}
shoes_merged['currency'] = shoes_merged['currency'].str.lower().map(currency_map)

print(shoes_merged.head())

# Forex file setup
forex_df['date'] = pd.to_datetime(forex_df['date'], errors='coerce')

# Filter forex data to only have EUR as base currency
forex_df = forex_df[forex_df['base_currency'] == 'EUR']

# Create dictionary for (currency, date) -> rate
forex_dict = {
    (row['currency'], row['date'].date()): row['exchange_rate']
    for _, row in forex_df.iterrows()
}

# Function to apply exchange rate
def apply_exchange_rate(row):
    if pd.isnull(row['price']) or pd.isnull(row['date']):
        return None
    if row['currency'].lower() in ['eur', 'euro']:
        return row['price']
    key = (row['currency'], row['date'].date())
    rate = forex_dict.get(key)
    if rate:
        return round(row['price'] / rate, 2)
    return None

# Apply conversion
print("Applying exchange rates locally...")
shoes_merged['standardized_price_euro'] = shoes_merged.progress_apply(apply_exchange_rate, axis=1)

# Output
print(shoes_merged[['price', 'currency', 'date', 'standardized_price_euro']].head())

# Shoe size conversion
conversion_men = {
    'usa': {'6': 39, '6.5': 39.5, '7': 40, '7.5': 40.5, '8': 41, '8.5': 41.5, '9': 42, '9.5': 42.5, '10': 43, '10.5': 44, '11': 44.5, '11.5': 45, '12': 46},
    'uk':  {'5.5': 39, '6': 39.5, '6.5': 40, '7': 41, '7.5': 41.5, '8': 42, '8.5': 42.5, '9': 43, '9.5': 44, '10': 44.5, '10.5': 45, '11': 46}
}

conversion_women = {
    'usa': {'4': 35, '4.5': 35.5, '5': 36, '5.5': 36.5, '6': 37, '6.5': 37.5, '7': 38, '7.5': 38.5, '8': 39, '8.5': 40, '9': 40.5, '9.5': 41, '10': 42},
    'uk':  {'2': 35, '2.5': 35.5, '3': 36, '3.5': 36.5, '4': 37, '4.5': 37.5, '5': 38, '5.5': 38.5, '6': 39, '6.5': 40, '7': 40.5, '7.5': 41, '8': 42}
}

conversion_kids = {
    'usa': {'10.5': 27.5, '11': 28, '11.5': 28.5, '12': 29, '12.5': 30, '13': 30.5, '13.5': 31, '1': 32, '1.5': 32.5, '2': 33, '2.5': 33.5, '3': 34},
    'uk':  {'10': 27.5, '10.5': 28, '11': 28.5, '11.5': 29, '12': 30, '12.5': 30.5, '13': 31, '13.5': 32, '1': 32.5, '1.5': 33, '2': 33.5, '2.5': 34}
}

conversion_all = {
    'M': conversion_men,
    'W': conversion_women,
    'U': {**conversion_men, **conversion_women},
    'K': conversion_kids
}

# Conversion function
def standardize_size(row):
    metric = str(row['shoe_metric']).lower().strip()
    size = str(row['size']).strip()
    gender = str(row['gender']).upper().strip()

    if metric == 'eu':
        return size
    
    if ' ' in size:
        size = size.split()[0]

    if metric == 'uk' and gender == 'K' and size.endswith('K'):
        size = size[:-1]

    gender = gender if gender in conversion_all else 'U'

    if metric in ['usa', 'uk']:
        return conversion_all[gender].get(metric, {}).get(size)
    return None

# Apply the size conversion
print("Applying shoe size conversions...")
shoes_merged['standardized_size_eu'] = shoes_merged.progress_apply(standardize_size, axis=1)

# Output
print(shoes_merged[['size', 'shoe_metric', 'gender', 'standardized_size_eu']].head())

country_subset = ['DE', 'US', 'UK', 'BE']
filtered_df = shoes_merged[shoes_merged['country_code'].isin(country_subset)]
sampled_df = filtered_df.groupby('country_code').apply(lambda x: x.head(10)).reset_index(drop=True)
print(sampled_df)

# Graph 5 shoes total availability on each date
shoes_merged['availability'] = pd.to_numeric(shoes_merged['availability'], errors='coerce')
shoes_merged = shoes_merged.dropna(subset=['availability', 'date'])

sample_ids = random.sample(list(shoes_merged['id'].unique()), 5)
id_name_map = shoes_dim.set_index('id')['name'].to_dict()

plt.figure(figsize=(12, 6))
for shoe_id in sample_ids:
    df_id = shoes_merged[shoes_merged['id'] == shoe_id]
    grouped = df_id.groupby('date')['availability'].sum()
    label = id_name_map.get(shoe_id, f"ID {shoe_id}")
    plt.plot(grouped.index, grouped.values, label=label)

plt.xlabel('Date')
plt.ylabel('Total Availability')
plt.title('Availability Over Time for 5 Random Shoes')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Export the final merged dataset to a CSV file (only inside repo now)
shoes_merged.to_csv(base_path + "final_shoes_merged.csv", index=False)
