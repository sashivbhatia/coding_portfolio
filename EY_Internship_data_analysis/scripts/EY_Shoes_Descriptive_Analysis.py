import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="colorblind", font_scale=1.2)

shoes_merged = pd.read_csv(r"C:\EY_Data\final_shoes_merged.csv", parse_dates=['date'])
shoes_dim = pd.read_csv(r"C:\EY_Data\shoes_dim.csv")
id_name_map = shoes_dim.set_index('id')['name'].to_dict()

#DESCRIPTIVE ANALYSIS BY SHOE MODEL
print("DESCRIPTIVE ANALYSIS BY SHOE MODEL")
print("-----------------------------------------")
print("")

# Q1: What are the top 5 most available shoe models overall?
total_availability = shoes_merged.groupby('id')['availability'].sum().sort_values(ascending=False).head(5)
top_availability = total_availability.reset_index()
top_availability['name'] = top_availability['id'].map(id_name_map)
top_availability.columns = ['id', 'total_availability', 'name']
print("Top 5 Shoe Models by Total Availability:")
print(top_availability[['name', 'total_availability']])
print("")

###

# Q2: What are the bottom 5 models by non-zero availability (not truly deadstock)?
non_zero_total = shoes_merged.groupby('id')['availability'].sum()
non_zero_total = non_zero_total[non_zero_total > 0].sort_values().head(5)
bottom_availability = non_zero_total.reset_index()
bottom_availability['name'] = bottom_availability['id'].map(id_name_map)
bottom_availability.columns = ['id', 'total_availability', 'name']
print("Bottom 5 Shoe Models by Non-Zero Total Availability:")
print(bottom_availability[['name', 'total_availability']])
print("")

###

# Q3: Which shoe models experienced the highest net sales (availability decrease)?
sorted_df = shoes_merged.sort_values(['id', 'date'])
sorted_df['availability_diff'] = sorted_df.groupby('id')['availability'].diff()
sales_by_id = sorted_df[sorted_df['availability_diff'] < 0].groupby('id')['availability_diff'].sum().abs()
top_sales = sales_by_id.sort_values(ascending=False).head(5).reset_index()
top_sales['name'] = top_sales['id'].map(id_name_map)
top_sales.columns = ['id', 'net_availability_decrease', 'name']
print("Top 5 Shoe Models by Net Decrease in Availability (Sales Proxy):")
print(top_sales[['name', 'net_availability_decrease']])
print("")

###

# Q4: Which shoe models are deadstock (no change in availability over time)?
availability_changes = shoes_merged.groupby('id')['availability'].nunique()
deadstock_ids = availability_changes[availability_changes == 1].index
deadstock_names = pd.DataFrame(deadstock_ids, columns=['id'])
deadstock_names['name'] = deadstock_names['id'].map(id_name_map)
print("Deadstock Shoe Models (No Availability Change):")
print(deadstock_names.head(5))
print("")

######

#DESCRIPTIVE ANALYSIS BY DEMOGRAPHICS
print("DESCRIPTIVE ANALYSIS BY DEMOGRAPHICS")
print("-----------------------------------------")
print("")

# Q5: What are the sell-out rates by gender?
sorted_df = shoes_merged.sort_values(['id', 'date'])
sorted_df['availability_diff'] = sorted_df.groupby('id')['availability'].diff()
decreases = sorted_df[sorted_df['availability_diff'] < 0]
net_decrease = decreases.groupby('gender')['availability_diff'].sum().abs()
first_date = sorted_df['date'].min()
initial_snapshot = sorted_df[sorted_df['date'] == first_date]
initial_availability = initial_snapshot.groupby('gender')['availability'].sum()
sellout_rate = (net_decrease / initial_availability).sort_values(ascending=False)
print("Normalized Net Decrease in Availability by Gender (Sell-Out Rate):")
print(sellout_rate)
print("")

###

# Q6: Which countries have the highest total sales (availability decrease)?
sorted_df = shoes_merged.sort_values(['country_code', 'id', 'date'])
sorted_df['availability_diff'] = sorted_df.groupby(['country_code', 'id'])['availability'].diff()
country_sales = sorted_df[sorted_df['availability_diff'] < 0].groupby('country_code')['availability_diff'].sum().abs()
top_countries = country_sales.sort_values(ascending=False)
print("Total Net Sales by Country (Net Availability Decrease):")
print(top_countries)
print("")

###

# Q7: Which countries show the greatest variation in sales volume across price segments?
bins = [0, 50, 100, 200, 500, np.inf]
labels = ['Budget (<50€)', 'Low (50-100€)', 'Mid (100-200€)', 'High (200-500€)', 'Premium (>500€)']
shoes_merged['price_segment'] = pd.cut(shoes_merged['standardized_price_euro'], bins=bins, labels=labels)
shoes_merged['availability_diff'] = shoes_merged.groupby(['id', 'country_code'])['availability'].diff()
shoes_merged['sales_volume'] = shoes_merged['availability_diff'].where(shoes_merged['availability_diff'] < 0, 0).abs()
segment_country_sales = shoes_merged.groupby(['country_code', 'price_segment'])['sales_volume'].sum().unstack(fill_value=0)
print("Sales Volume by Price Segment and Country:")
print(segment_country_sales)
print("")

#DESCRIPTIVE ANALYSIS FOR OTHER
print("DESCRIPTIVE ANALYSIS FOR OTHER")
print("-----------------------------------------")
print("")

# Q8: Is there a statistically significant correlation between standardized price and total sales volume?
price_sales_df = shoes_merged.copy()
price_sales_df['availability_diff'] = price_sales_df.groupby('id')['availability'].diff()
price_sales_df['negative_diff'] = price_sales_df['availability_diff'].where(price_sales_df['availability_diff'] < 0, 0)
total_sales = price_sales_df.groupby('id')['negative_diff'].sum().abs().rename('total_sales')
avg_price = shoes_merged.groupby('id')['standardized_price_euro'].mean().rename('avg_price_eur')
correlation_df = pd.concat([total_sales, avg_price], axis=1).dropna()
correlation = correlation_df['avg_price_eur'].corr(correlation_df['total_sales'])
slope, intercept = np.polyfit(correlation_df['avg_price_eur'], correlation_df['total_sales'], 1)
print("Correlation between Average Price (EUR) and Total Sales Volume:")
print(f"Pearson Correlation Coefficient: {correlation:.4f}")
print(f"Linear Regression Equation: total_sales = {slope:.4f} * avg_price_eur + {intercept:.2f}")
print("")

###

# Q9: Do higher-priced shoes tend to remain in deadstock longer than lower-priced ones?
availability_changes = shoes_merged.groupby('id')['availability'].nunique()
deadstock_ids = availability_changes[availability_changes == 1].index
active_ids = availability_changes[availability_changes > 1].index
deadstock_prices = shoes_merged[shoes_merged['id'].isin(deadstock_ids)].groupby('id')['standardized_price_euro'].mean()
active_prices = shoes_merged[shoes_merged['id'].isin(active_ids)].groupby('id')['standardized_price_euro'].mean()
print("Deadstock Shoe Models – Price Statistics:")
print(f"Mean: {deadstock_prices.mean():.2f} EUR")
print(f"Median: {deadstock_prices.median():.2f} EUR")
print("")
print("\nActive Seller Shoe Models – Price Statistics:")
print(f"Mean: {active_prices.mean():.2f} EUR")
print(f"Median: {active_prices.median():.2f} EUR")
print("")


####################################################################################################
# NEW AND IMPROVED VISUALIZATION SECTION
####################################################################################################

# Prepare the figure for a 3x3 grid of plots
fig, axes = plt.subplots(3, 3, figsize=(20, 18)) # Set a larger figure size for better readability
fig.suptitle('Shoe Data Analysis: Key Insights Visualization', fontsize=22, y=1.02, weight='bold') # Main title for the entire grid
axes = axes.flatten() # Flatten the 2D array of axes for easy iteration

# --- Question 1: Top 5 Most Available Shoe Models ---
# Visualization: Horizontal Bar Plot for clear ranking
sns.barplot(x='total_availability', y='name', data=top_availability, ax=axes[0], palette='Blues_d')
axes[0].set_title("Question 1: Top 5 Most Available Models", fontsize=14, weight='bold')
axes[0].set_xlabel("Total Availability", fontsize=12)
axes[0].set_ylabel("Shoe Model Name", fontsize=12)
axes[0].tick_params(axis='y', labelsize=10) # Adjust label size for long names

# --- Question 2: Bottom 5 Models by Non-Zero Availability ---
# Visualization: Horizontal Bar Plot to show the lowest availability models
sns.barplot(x='total_availability', y='name', data=bottom_availability, ax=axes[1], palette='Reds_d')
axes[1].set_title("Question 2: Bottom 5 Non-Zero Availability Models", fontsize=14, weight='bold')
axes[1].set_xlabel("Total Availability", fontsize=12)
axes[1].set_ylabel("Shoe Model Name", fontsize=12)
axes[1].tick_params(axis='y', labelsize=10)

# --- Question 3: Top 5 Models by Net Sales (Availability Decrease) ---
# Visualization: Horizontal Bar Plot to highlight models with highest sales
sns.barplot(x='net_availability_decrease', y='name', data=top_sales, ax=axes[2], palette='Greens_d')
axes[2].set_title("Question 3: Top 5 Models by Net Sales", fontsize=14, weight='bold')
axes[2].set_xlabel("Net Availability Decrease (Sales)", fontsize=12)
axes[2].set_ylabel("Shoe Model Name", fontsize=12)
axes[2].tick_params(axis='y', labelsize=10)

# --- Question 4: Deadstock vs. Active Shoe Models ---
# Visualization: Bar plot to compare the counts of deadstock vs. active models
model_status_counts = pd.DataFrame({
    'Status': ['Deadstock', 'Active'],
    'Count': [len(deadstock_ids), len(active_ids)]
})
sns.barplot(x='Status', y='Count', data=model_status_counts, ax=axes[3], palette='Pastel1')
axes[3].set_title("Question 4: Deadstock vs. Active Models Count", fontsize=14, weight='bold')
axes[3].set_xlabel("Model Status", fontsize=12)
axes[3].set_ylabel("Number of Models", fontsize=12)
# Add count labels on top of bars for clarity
for p in axes[3].patches:
    axes[3].annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=10)


# --- Question 5: Sell-Out Rates by Gender ---
# Visualization: Bar plot to show gender-wise sell-out rates
sellout_rate_df = sellout_rate.reset_index()
sellout_rate_df.columns = ['Gender', 'SellOutRate']
sns.barplot(x='Gender', y='SellOutRate', data=sellout_rate_df, ax=axes[4], palette='coolwarm')
axes[4].set_title("Question 5: Sell-Out Rates by Gender", fontsize=14, weight='bold')
axes[4].set_xlabel("Gender", fontsize=12)
axes[4].set_ylabel("Sell-Out Rate", fontsize=12)
axes[4].set_ylim(0, sellout_rate_df['SellOutRate'].max() * 1.1) # Adjust y-limit for better visualization
# Add percentage labels on top of bars
for p in axes[4].patches:
    axes[4].annotate(f'{p.get_height():.2%}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=10)


# --- Question 6: Total Sales by Country ---
# Visualization: Horizontal Bar Plot for country-wise sales ranking
top_countries_df = top_countries.reset_index()
top_countries_df.columns = ['Country', 'TotalSales']
sns.barplot(x='TotalSales', y='Country', data=top_countries_df, ax=axes[5], palette='Spectral')
axes[5].set_title("Question 6: Total Sales by Country", fontsize=14, weight='bold')
axes[5].set_xlabel("Total Sales (Availability Decrease)", fontsize=12)
axes[5].set_ylabel("Country Code", fontsize=12)

# --- Question 7: Sales Volume by Country & Price Segment ---
# Visualization: Grouped Bar Plot to compare sales across segments within countries
# Melt the DataFrame to long format for Seaborn's hue parameter
segment_country_sales_melted = segment_country_sales.reset_index().melt(id_vars='country_code', var_name='price_segment', value_name='sales_volume')
# Ensure price_segment order is maintained for consistent plotting
segment_country_sales_melted['price_segment'] = pd.Categorical(segment_country_sales_melted['price_segment'], categories=labels, ordered=True)

sns.barplot(x='country_code', y='sales_volume', hue='price_segment', data=segment_country_sales_melted, ax=axes[6], palette='tab10')
axes[6].set_title("Question 7: Sales Volume by Country & Price Segment", fontsize=14, weight='bold')
axes[6].set_xlabel("Country Code", fontsize=12)
axes[6].set_ylabel("Sales Volume", fontsize=12)
axes[6].legend(title='Price Segment', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=10, title_fontsize=12) # Move legend outside the plot area

# --- Question 8: Correlation between Price and Total Sales Volume ---
# Visualization: Scatter Plot with a Regression Line to show correlation
sns.regplot(x='avg_price_eur', y='total_sales', data=correlation_df, ax=axes[7], scatter_kws={'alpha':0.6}, line_kws={'color':'red', 'linestyle':'--'})
axes[7].set_title(f"Question 8: Price vs. Total Sales (Corr: {correlation:.2f})", fontsize=14, weight='bold')
axes[7].set_xlabel("Average Price (EUR)", fontsize=12)
axes[7].set_ylabel("Total Sales Volume", fontsize=12)

# --- Question 9: Price Distribution of Deadstock vs. Active Models ---
# Visualization: Box Plot to compare price distributions
# Combine deadstock and active prices into a single DataFrame for plotting
deadstock_df = pd.DataFrame({'price': deadstock_prices, 'status': 'Deadstock'})
active_df = pd.DataFrame({'price': active_prices, 'status': 'Active'})
combined_prices_df = pd.concat([deadstock_df, active_df])

sns.boxplot(x='status', y='price', data=combined_prices_df, ax=axes[8], palette='Set2')
axes[8].set_title("Question 9: Price Distribution by Model Status", fontsize=14, weight='bold')
axes[8].set_xlabel("Model Status", fontsize=12)
axes[8].set_ylabel("Average Price (EUR)", fontsize=12)


# Adjust layout to prevent overlapping titles/labels and show the plot
plt.tight_layout(rect=[0, 0.03, 1, 0.98]) # Adjust rect to make space for the main suptitle
plt.show()
