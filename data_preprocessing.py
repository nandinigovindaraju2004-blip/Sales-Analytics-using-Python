"""
============================================================
  Season-wise & Region-wise Product Sales Analytics
  Module: Data Preprocessing & EDA
  Author: MCA Project
============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────
def load_data(path='data/sales_data.csv'):
    df = pd.read_csv(path)
    print(f"✅ Loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    return df

# ─────────────────────────────────────────
# 2. DATA CLEANING
# ─────────────────────────────────────────
def clean_data(df):
    print("\n── Data Cleaning ──")

    # Check missing values
    missing = df.isnull().sum()
    print(f"Missing values:\n{missing[missing > 0]}")

    # Fill numeric missing values with median
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if df[col].isnull().any():
            df[col].fillna(df[col].median(), inplace=True)

    # Fill categorical missing values with mode
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df[col].isnull().any():
            df[col].fillna(df[col].mode()[0], inplace=True)

    # Remove duplicates
    before = len(df)
    df.drop_duplicates(subset='Order_ID', inplace=True)
    print(f"Duplicates removed: {before - len(df)}")

    # Parse dates
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Ship_Date'] = pd.to_datetime(df['Ship_Date'])

    # Ensure numeric types
    for col in ['Sales', 'Profit', 'Cost', 'Quantity', 'Discount']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Remove negative sales
    df = df[df['Sales'] > 0]

    print(f"✅ Clean dataset: {df.shape[0]} rows")
    return df

# ─────────────────────────────────────────
# 3. FEATURE ENGINEERING
# ─────────────────────────────────────────
def feature_engineering(df):
    print("\n── Feature Engineering ──")
    df['Profit_Margin'] = (df['Profit'] / df['Sales'] * 100).round(2)
    df['Revenue_per_Unit'] = (df['Sales'] / df['Quantity']).round(2)
    df['Ship_Days'] = (df['Ship_Date'] - df['Order_Date']).dt.days
    df['YearMonth'] = df['Order_Date'].dt.to_period('M').astype(str)
    df['Week'] = df['Order_Date'].dt.isocalendar().week.astype(int)
    df['Is_Profitable'] = (df['Profit'] > 0).astype(int)
    season_order = {'Winter': 1, 'Spring': 2, 'Summer': 3, 'Autumn': 4}
    df['Season_Order'] = df['Season'].map(season_order)
    print("✅ New features added: Profit_Margin, Revenue_per_Unit, Ship_Days, YearMonth, Week, Is_Profitable")
    return df

# ─────────────────────────────────────────
# 4. EDA SUMMARY
# ─────────────────────────────────────────
def eda_summary(df):
    print("\n── EDA Summary ──")
    print(f"Total Sales     : ₹{df['Sales'].sum():,.2f}")
    print(f"Total Profit    : ₹{df['Profit'].sum():,.2f}")
    print(f"Avg Profit Margin: {df['Profit_Margin'].mean():.2f}%")
    print(f"Total Orders    : {len(df):,}")
    print(f"Unique Products : {df['Product_Name'].nunique()}")
    print(f"Regions         : {df['Region'].unique()}")
    print(f"Categories      : {df['Category'].unique()}")
    print(f"Years Covered   : {sorted(df['Year'].unique())}")

    print("\n── Top 5 Products by Sales ──")
    top5 = df.groupby('Product_Name')['Sales'].sum().nlargest(5)
    print(top5)

    print("\n── Sales by Season ──")
    season_sales = df.groupby('Season')['Sales'].sum().sort_values(ascending=False)
    print(season_sales)

    print("\n── Sales by Region ──")
    region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    print(region_sales)

    return df

# ─────────────────────────────────────────
# 5. VISUALIZATIONS
# ─────────────────────────────────────────
def create_visualizations(df, output_dir='reports'):
    import os
    os.makedirs(output_dir, exist_ok=True)

    plt.style.use('seaborn-v0_8-darkgrid')
    colors = ['#00D4FF', '#7B2FBE', '#FF6B6B', '#00C853', '#FFD700']

    # ── Chart 1: Top 10 Products by Sales
    fig, ax = plt.subplots(figsize=(12, 6))
    top10 = df.groupby('Product_Name')['Sales'].sum().nlargest(10).sort_values()
    bars = ax.barh(top10.index, top10.values, color=colors * 2)
    ax.set_xlabel('Total Sales (₹)', fontsize=12)
    ax.set_title('🏆 Top 10 Products by Sales', fontsize=16, fontweight='bold', pad=20)
    for bar in bars:
        ax.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
                f'₹{bar.get_width():,.0f}', va='center', fontsize=8)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top_products.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Chart 2: Season-wise Sales
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    season_data = df.groupby('Season')['Sales'].sum().reindex(['Spring','Summer','Autumn','Winter'])
    axes[0].bar(season_data.index, season_data.values, color=colors[:4], edgecolor='white', linewidth=1.5)
    axes[0].set_title('📅 Season-wise Total Sales', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Sales (₹)')
    for i, v in enumerate(season_data.values):
        axes[0].text(i, v + 5000, f'₹{v:,.0f}', ha='center', fontsize=9, fontweight='bold')

    season_profit = df.groupby('Season')['Profit'].sum().reindex(['Spring','Summer','Autumn','Winter'])
    axes[1].bar(season_profit.index, season_profit.values, color=colors[1:], edgecolor='white', linewidth=1.5)
    axes[1].set_title('📅 Season-wise Profit', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Profit (₹)')
    plt.suptitle('Seasonal Sales Performance', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/season_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Chart 3: Region-wise Sales (Pie + Bar)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    region_data = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    axes[0].pie(region_data.values, labels=region_data.index, autopct='%1.1f%%',
                colors=colors, startangle=140, textprops={'fontsize':11})
    axes[0].set_title('🌍 Region-wise Sales Distribution', fontsize=14, fontweight='bold')
    axes[1].bar(region_data.index, region_data.values, color=colors)
    axes[1].set_title('🌍 Region-wise Sales Comparison', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Total Sales (₹)')
    for i, v in enumerate(region_data.values):
        axes[1].text(i, v + 1000, f'₹{v:,.0f}', ha='center', fontsize=9, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/region_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Chart 4: Monthly Revenue Trend
    fig, ax = plt.subplots(figsize=(14, 6))
    monthly = df.groupby('YearMonth')['Sales'].sum().reset_index()
    monthly = monthly.sort_values('YearMonth')
    ax.plot(range(len(monthly)), monthly['Sales'], color='#00D4FF', linewidth=2.5, marker='o', markersize=4)
    ax.fill_between(range(len(monthly)), monthly['Sales'], alpha=0.2, color='#00D4FF')
    ax.set_xticks(range(0, len(monthly), 3))
    ax.set_xticklabels(monthly['YearMonth'].iloc[::3], rotation=45, ha='right')
    ax.set_title('📈 Monthly Revenue Trend (2021–2024)', fontsize=16, fontweight='bold')
    ax.set_ylabel('Sales (₹)')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/monthly_trend.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Chart 5: Category-wise Heatmap (Region × Category)
    fig, ax = plt.subplots(figsize=(12, 6))
    pivot = df.pivot_table(values='Sales', index='Region', columns='Category', aggfunc='sum')
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax,
                linewidths=0.5, cbar_kws={'label': 'Sales (₹)'})
    ax.set_title('🔥 Region × Category Sales Heatmap', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Chart 6: Profit Margin by Category
    fig, ax = plt.subplots(figsize=(10, 6))
    cat_margin = df.groupby('Category')['Profit_Margin'].mean().sort_values(ascending=False)
    bars = ax.bar(cat_margin.index, cat_margin.values, color=colors, edgecolor='white', linewidth=1.5)
    ax.set_title('💰 Average Profit Margin by Category', fontsize=16, fontweight='bold')
    ax.set_ylabel('Profit Margin (%)')
    ax.axhline(y=cat_margin.mean(), color='red', linestyle='--', label=f'Avg: {cat_margin.mean():.1f}%')
    ax.legend()
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                f'{bar.get_height():.1f}%', ha='center', fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/profit_margin.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Chart 7: Year-over-Year Comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    yearly = df.groupby(['Year', 'Season'])['Sales'].sum().unstack()
    yearly.plot(kind='bar', ax=ax, color=colors[:4], edgecolor='white', linewidth=0.5, width=0.7)
    ax.set_title('📊 Year-over-Year Seasonal Sales Comparison', fontsize=16, fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Sales (₹)')
    ax.legend(title='Season', bbox_to_anchor=(1.01, 1))
    ax.set_xticklabels(yearly.index, rotation=0)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/yoy_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()

    # ── Chart 8: Correlation Heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    corr_cols = ['Sales', 'Profit', 'Cost', 'Quantity', 'Discount', 'Profit_Margin', 'Ship_Days']
    corr = df[corr_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                ax=ax, vmin=-1, vmax=1, center=0, linewidths=0.5)
    ax.set_title('🔗 Correlation Matrix', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/correlation.png', dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✅ All charts saved to {output_dir}/")

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == '__main__':
    df = load_data('data/sales_data.csv')
    df = clean_data(df)
    df = feature_engineering(df)
    df = eda_summary(df)
    create_visualizations(df)
    df.to_csv('data/cleaned_sales_data.csv', index=False)
    print("\n✅ Cleaned dataset saved.")