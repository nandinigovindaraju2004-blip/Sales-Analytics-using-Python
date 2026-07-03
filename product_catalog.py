"""
============================================================
  Product Catalog Generator
  Generates Meesho-style catalog metadata: star ratings,
  review counts, MRP/discount pricing, and product images
  for every unique product in the sales dataset.
============================================================
"""

import pandas as pd
import numpy as np
import hashlib

np.random.seed(7)

# Real, freely-embeddable product photos (Unsplash, direct CDN links).
# One curated image per product — picked to visually match the product name.
PRODUCT_IMAGES = {
    # Electronics
    'iPhone 15': 'https://images.unsplash.com/photo-1592286927505-7ed27a4c80f8?w=500&q=80',
    'Samsung Galaxy': 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=500&q=80',
    'iPad Air': 'https://images.unsplash.com/photo-1561154464-82e9adf32764?w=500&q=80',
    'MacBook Pro': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&q=80',
    'Dell Laptop': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&q=80',
    'Sony Headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80',
    'Canon Camera': 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=500&q=80',
    'LG Monitor': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500&q=80',
    # Furniture
    'Executive Chair': 'https://images.unsplash.com/photo-1505843490578-d3ec9e6d5f8c?w=500&q=80',
    'Standing Desk': 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=500&q=80',
    'Bookshelf': 'https://images.unsplash.com/photo-1594620302200-9a762244a156?w=500&q=80',
    'Filing Cabinet': 'https://images.unsplash.com/photo-1591129841117-3adfd313e34f?w=500&q=80',
    'Conference Table': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=500&q=80',
    'Ergonomic Chair': 'https://images.unsplash.com/photo-1505843490701-5be5d1b31f8f?w=500&q=80',
    'Reception Desk': 'https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=500&q=80',
    # Office Supplies
    'A4 Paper Pack': 'https://images.unsplash.com/photo-1517842645767-c639042777db?w=500&q=80',
    'Ballpoint Pens': 'https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=500&q=80',
    'Sticky Notes': 'https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=500&q=80',
    'Stapler Set': 'https://images.unsplash.com/photo-1568205612837-017257d2da8b?w=500&q=80',
    'Notebooks Bundle': 'https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=500&q=80',
    'Highlighters': 'https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=500&q=80',
    'File Folders': 'https://images.unsplash.com/photo-1568205612837-017257d2da8b?w=500&q=80',
    # Clothing
    'Business Shirt': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500&q=80',
    'Formal Trousers': 'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=500&q=80',
    'Running Shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80',
    'Winter Jacket': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&q=80',
    'Sport Socks': 'https://images.unsplash.com/photo-1586350977771-b3b0abd50c82?w=500&q=80',
    'Casual T-Shirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&q=80',
    # Sports
    'Yoga Mat': 'https://images.unsplash.com/photo-1592432678016-e910b452f9a2?w=500&q=80',
    'Dumbbells Set': 'https://images.unsplash.com/photo-1638536532686-d610adfc8e5c?w=500&q=80',
    'Running Shoes Pro': 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500&q=80',
    'Fitness Tracker': 'https://images.unsplash.com/photo-1576243345690-4e4b79b63288?w=500&q=80',
    'Protein Powder': 'https://images.unsplash.com/photo-1579722820308-13f1981fa7e5?w=500&q=80',
    'Jump Rope': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500&q=80',
    'Resistance Bands': 'https://images.unsplash.com/photo-1598971639058-fab3c3109a00?w=500&q=80',
}

FALLBACK_IMAGE = 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=500&q=80'


def _seeded_rng(name):
    """Deterministic per-product RNG so ratings stay stable across reruns."""
    seed = int(hashlib.md5(name.encode()).hexdigest()[:8], 16) % (2**32 - 1)
    return np.random.RandomState(seed)


def generate_catalog(df):
    """
    Build one catalog row per unique product with:
    - Star rating (3.5 - 5.0)
    - Review count
    - MRP, selling price, discount %
    - Product image URL
    - Badges (Bestseller / Trending / New)
    """
    products = df.groupby('Product_Name').agg(
        Category=('Category', 'first'),
        Sub_Category=('Sub_Category', 'first'),
        Avg_Unit_Price=('Unit_Price', 'mean'),
        Total_Sales=('Sales', 'sum'),
        Total_Quantity=('Quantity', 'sum'),
        Avg_Discount=('Discount', 'mean'),
        Order_Count=('Order_ID', 'count'),
    ).reset_index()

    rows = []
    for _, r in products.iterrows():
        rng = _seeded_rng(r['Product_Name'])

        # Star rating: weighted toward 3.8 - 4.8, occasional 5.0
        rating = round(min(5.0, max(3.5, rng.normal(4.2, 0.35))), 1)

        # Review count loosely tied to actual order volume for realism
        review_count = int(r['Order_Count'] * rng.uniform(8, 22))

        # Pricing: MRP is the "original" price, selling price reflects avg discount
        mrp = round(r['Avg_Unit_Price'] * rng.uniform(1.15, 1.45), 2)
        discount_pct = round(max(r['Avg_Discount'] * 100, rng.uniform(5, 15)), 0)
        selling_price = round(mrp * (1 - discount_pct / 100), 2)

        # Badge logic
        if r['Total_Sales'] >= products['Total_Sales'].quantile(0.85):
            badge = 'Bestseller'
        elif r['Order_Count'] >= products['Order_Count'].quantile(0.7):
            badge = 'Trending'
        elif rng.random() < 0.15:
            badge = 'New'
        else:
            badge = None

        rows.append({
            'Product_Name': r['Product_Name'],
            'Category': r['Category'],
            'Sub_Category': r['Sub_Category'],
            'Image_URL': PRODUCT_IMAGES.get(r['Product_Name'], FALLBACK_IMAGE),
            'Rating': rating,
            'Review_Count': review_count,
            'MRP': mrp,
            'Selling_Price': selling_price,
            'Discount_Pct': int(discount_pct),
            'Total_Sales': round(r['Total_Sales'], 2),
            'Total_Quantity_Sold': int(r['Total_Quantity']),
            'Badge': badge,
        })

    catalog = pd.DataFrame(rows).sort_values('Total_Sales', ascending=False).reset_index(drop=True)
    return catalog


if __name__ == '__main__':
    df = pd.read_csv('data/sales_data.csv')
    catalog = generate_catalog(df)
    catalog.to_csv('data/product_catalog.csv', index=False)
    print(f"✅ Catalog generated: {len(catalog)} products")
    print(catalog[['Product_Name', 'Category', 'Rating', 'Review_Count', 'MRP', 'Selling_Price', 'Discount_Pct', 'Badge']].head(10).to_string(index=False))
