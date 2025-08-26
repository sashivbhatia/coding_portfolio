import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import os
from datetime import datetime

sns.set_theme(style="whitegrid", palette="colorblind", font_scale=1.2)

shoes_merged = pd.read_csv(r"C:\UW\Github\coding_portfolio\EY_Internship_data_analysis\data\final_shoes_merged.csv", parse_dates=['date'])
shoes_dim = pd.read_csv(r"C:\UW\Github\coding_portfolio\EY_Internship_data_analysis\data\shoes_dim.csv")
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

# ==============================
# PDF Report Generation
# ==============================

# Ensure results folder exists
results_dir = r"C:\UW\Github\coding_portfolio\EY_Internship_data_analysis\results"
os.makedirs(results_dir, exist_ok=True)

# Auto timestamp filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
pdf_path = os.path.join(results_dir, f"shoe_analysis_report_{timestamp}.pdf")

# Helper: truncate names
def truncate_name(name, length=30):
    return name if len(name) <= length else name[:length-3] + "..."

# Apply truncation
top_availability['short_name']    = top_availability['name'].apply(truncate_name)
bottom_availability['short_name'] = bottom_availability['name'].apply(truncate_name)
top_sales['short_name']           = top_sales['name'].apply(truncate_name)

# Write plots into PDF (all pages portrait + fixes for labels/legend)
with PdfPages(pdf_path) as pdf:

    # === TITLE PAGE (portrait) ===
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis("off")
    plt.text(
        0.5, 0.60,
        "EY Internship Project:\nExploratory Analysis of Global Shoe Market Trends",
        fontsize=22, ha="center", va="center", fontweight="bold"
    )
    plt.text(0.5, 0.46, "Sashiv Bhatia", fontsize=14, ha="center", va="center")
    pdf.savefig(fig); plt.close(fig)

    # --- Q1: Top 5 Most Available Models (VERTICAL barplot) ---
    fig, ax = plt.subplots(figsize=(8.5, 11))
    sns.barplot(x='short_name', y='total_availability', data=top_availability,
                palette='Blues_d', ax=ax)
    ax.set_title("Q1: Top 5 Most Available Models", fontsize=16, fontweight='bold')
    ax.set_xlabel("Shoe Model (≤30 chars)")
    ax.set_ylabel("Total Availability")
    ax.tick_params(axis='x', rotation=45, labelsize=9)
    plt.subplots_adjust(left=0.15, right=0.96, top=0.90, bottom=0.25)
    pdf.savefig(fig); plt.close(fig)

    # --- Q2: Bottom 5 Non-Zero Availability Models (VERTICAL barplot) ---
    fig, ax = plt.subplots(figsize=(8.5, 11))
    sns.barplot(x='short_name', y='total_availability', data=bottom_availability,
                palette='Reds_d', ax=ax)
    ax.set_title("Q2: Bottom 5 Non-Zero Availability Models", fontsize=16, fontweight='bold')
    ax.set_xlabel("Shoe Model (≤30 chars)")
    ax.set_ylabel("Total Availability")
    ax.tick_params(axis='x', rotation=45, labelsize=9)
    plt.subplots_adjust(left=0.15, right=0.96, top=0.90, bottom=0.25)
    pdf.savefig(fig); plt.close(fig)

    # --- Q3: Top 5 Models by Net Sales (VERTICAL barplot) ---
    fig, ax = plt.subplots(figsize=(8.5, 11))
    sns.barplot(x='short_name', y='net_availability_decrease', data=top_sales,
                palette='Greens_d', ax=ax)
    ax.set_title("Q3: Top 5 Models by Net Sales", fontsize=16, fontweight='bold')
    ax.set_xlabel("Shoe Model (≤30 chars)")
    ax.set_ylabel("Net Availability Decrease (Sales)")
    ax.tick_params(axis='x', rotation=45, labelsize=9)
    plt.subplots_adjust(left=0.15, right=0.96, top=0.90, bottom=0.25)
    pdf.savefig(fig); plt.close(fig)

    # --- Q4: Deadstock vs Active Models (portrait) ---
    fig, ax = plt.subplots(figsize=(8.5, 11))
    model_status_counts = pd.DataFrame({'Status': ['Deadstock','Active'],
                                        'Count':[len(deadstock_ids), len(active_ids)]})
    sns.barplot(x='Status', y='Count', data=model_status_counts, palette='Pastel1', ax=ax)
    ax.set_title("Q4: Deadstock vs Active Models Count", fontsize=16, fontweight='bold')
    ax.set_xlabel("Model Status"); ax.set_ylabel("Number of Models")
    for p in ax.patches:
        ax.text(p.get_x()+p.get_width()/2., p.get_height(), f'{int(p.get_height())}',
                ha='center', va='bottom')
    plt.subplots_adjust(left=0.12, right=0.96, top=0.90, bottom=0.12)
    pdf.savefig(fig); plt.close(fig)

    # --- Q5: Sell-Out Rates by Gender (portrait) ---
    fig, ax = plt.subplots(figsize=(8.5, 11))
    sellout_rate_df = sellout_rate.reset_index()
    sellout_rate_df.columns = ['Gender','SellOutRate']
    sns.barplot(x='Gender', y='SellOutRate', data=sellout_rate_df, palette='coolwarm', ax=ax)
    ax.set_title("Q5: Sell-Out Rates by Gender", fontsize=16, fontweight='bold')
    ax.set_xlabel("Gender"); ax.set_ylabel("Sell-Out Rate")
    ax.set_ylim(0, sellout_rate_df['SellOutRate'].max() * 1.15)
    for p in ax.patches:
        ax.text(p.get_x()+p.get_width()/2., p.get_height(), f'{p.get_height():.2%}',
                ha='center', va='bottom')
    plt.subplots_adjust(left=0.12, right=0.96, top=0.90, bottom=0.12)
    pdf.savefig(fig); plt.close(fig)

    # --- Q6: Total Sales by Country (VERTICAL barplot) ---
    fig, ax = plt.subplots(figsize=(8.5, 11))
    top_countries_df = top_countries.reset_index()
    top_countries_df.columns = ['Country','TotalSales']
    sns.barplot(x='Country', y='TotalSales', data=top_countries_df, palette='Spectral', ax=ax)
    ax.set_title("Q6: Total Sales by Country", fontsize=16, fontweight='bold')
    ax.set_xlabel("Country Code"); ax.set_ylabel("Total Sales (Availability Decrease)")
    ax.tick_params(axis='x', rotation=45, labelsize=9)
    plt.subplots_adjust(left=0.15, right=0.96, top=0.90, bottom=0.20)
    pdf.savefig(fig); plt.close(fig)

    # --- Q7: Sales Volume by Country & Price Segment (portrait, legend to right) ---
    fig, ax = plt.subplots(figsize=(8.5, 11))
    melted = segment_country_sales.reset_index().melt(
        id_vars='country_code', var_name='price_segment', value_name='sales_volume')
    melted['price_segment'] = pd.Categorical(melted['price_segment'],
                                             categories=labels, ordered=True)
    sns.barplot(x='country_code', y='sales_volume', hue='price_segment',
                data=melted, palette='tab10', ax=ax)
    ax.set_title("Q7: Sales Volume by Country & Price Segment", fontsize=16, fontweight='bold')
    ax.set_xlabel("Country Code"); ax.set_ylabel("Sales Volume")

    # Legend: half size, lower, to the right under the title
    ax.legend(
        title='Price Segment', loc='upper right', bbox_to_anchor=(1.0, 0.88),
        fontsize=8, title_fontsize=9, frameon=True
    )

    plt.subplots_adjust(left=0.12, right=0.96, top=0.86, bottom=0.12)
    pdf.savefig(fig); plt.close(fig)

    # --- Q8: Price vs Total Sales (portrait) ---
    fig, ax = plt.subplots(figsize=(8.5, 11))
    sns.regplot(x='avg_price_eur', y='total_sales', data=correlation_df,
                scatter_kws={'alpha':0.6}, line_kws={'color':'red','linestyle':'--'}, ax=ax)
    ax.set_title(f"Q8: Price vs Total Sales (Corr={correlation:.2f})",
                 fontsize=16, fontweight='bold')
    ax.set_xlabel("Average Price (EUR)"); ax.set_ylabel("Total Sales Volume")
    plt.subplots_adjust(left=0.12, right=0.96, top=0.90, bottom=0.12)
    pdf.savefig(fig); plt.close(fig)

    # --- Q9: Price Distribution by Model Status (portrait) ---
    fig, ax = plt.subplots(figsize=(8.5, 11))
    deadstock_df = pd.DataFrame({'price':deadstock_prices,'status':'Deadstock'})
    active_df   = pd.DataFrame({'price':active_prices,  'status':'Active'})
    combined    = pd.concat([deadstock_df, active_df])
    sns.boxplot(x='status', y='price', data=combined, palette='Set2', ax=ax)
    ax.set_title("Q9: Price Distribution by Model Status", fontsize=16, fontweight='bold')
    ax.set_xlabel("Model Status"); ax.set_ylabel("Average Price (EUR)")
    plt.subplots_adjust(left=0.12, right=0.96, top=0.90, bottom=0.12)
    pdf.savefig(fig); plt.close(fig)

print(f"✅ PDF report generated: {pdf_path}")
