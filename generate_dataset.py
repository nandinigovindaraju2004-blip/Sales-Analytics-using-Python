import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

regions = ['East', 'West', 'North', 'South', 'Central']
categories = ['Electronics', 'Furniture', 'Office Supplies', 'Clothing', 'Sports']
sub_categories = {
    'Electronics': ['Laptops', 'Phones', 'Tablets', 'Accessories', 'Cameras'],
    'Furniture': ['Chairs', 'Tables', 'Sofas', 'Shelves', 'Desks'],
    'Office Supplies': ['Pens', 'Paper', 'Folders', 'Staplers', 'Notebooks'],
    'Clothing': ['Shirts', 'Trousers', 'Shoes', 'Jackets', 'Accessories'],
    'Sports': ['Equipment', 'Shoes', 'Clothing', 'Accessories', 'Nutrition'],
}
products = {
    'Electronics': ['MacBook Pro', 'iPhone 15', 'iPad Air', 'Samsung Galaxy', 'Canon Camera', 'Dell Laptop', 'Sony Headphones', 'LG Monitor'],
    'Furniture': ['Executive Chair', 'Standing Desk', 'Bookshelf', 'Filing Cabinet', 'Conference Table', 'Ergonomic Chair', 'Reception Desk'],
    'Office Supplies': ['A4 Paper Pack', 'Ballpoint Pens', 'Sticky Notes', 'Stapler Set', 'Notebooks Bundle', 'Highlighters', 'File Folders'],
    'Clothing': ['Business Shirt', 'Formal Trousers', 'Running Shoes', 'Winter Jacket', 'Sport Socks', 'Casual T-Shirt'],
    'Sports': ['Yoga Mat', 'Dumbbells Set', 'Running Shoes Pro', 'Fitness Tracker', 'Protein Powder', 'Jump Rope', 'Resistance Bands'],
}
segments = ['Consumer', 'Corporate', 'Home Office']
ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']

def get_season(month):
    if month in [12,1,2]: return 'Winter'
    elif month in [3,4,5]: return 'Spring'
    elif month in [6,7,8]: return 'Summer'
    else: return 'Autumn'

rows = []
order_id = 1000
start = datetime(2021, 1, 1)
end = datetime(2024, 12, 31)

for _ in range(5000):
    order_date = start + timedelta(days=random.randint(0, (end-start).days))
    ship_date = order_date + timedelta(days=random.randint(1,7))
    category = random.choice(categories)
    product = random.choice(products[category])
    sub_cat = random.choice(sub_categories[category])
    region = random.choice(regions)
    segment = random.choice(segments)
    quantity = random.randint(1,20)
    base_prices = {'Electronics':500,'Furniture':300,'Office Supplies':30,'Clothing':80,'Sports':60}
    base = base_prices[category]
    price = round(base * random.uniform(0.5,3.0), 2)
    discount = round(random.choice([0,0,0,0.05,0.1,0.15,0.2,0.25,0.3]), 2)
    sales = round(price * quantity * (1-discount), 2)
    cost = round(sales * random.uniform(0.4, 0.75), 2)
    profit = round(sales - cost, 2)
    rows.append({
        'Order_ID': f'ORD-{order_id}',
        'Order_Date': order_date.strftime('%Y-%m-%d'),
        'Ship_Date': ship_date.strftime('%Y-%m-%d'),
        'Ship_Mode': random.choice(ship_modes),
        'Customer_ID': f'CUST-{random.randint(1000,9999)}',
        'Customer_Name': f'Customer_{random.randint(1,500)}',
        'Segment': segment,
        'Region': region,
        'State': f'{region}_State_{random.randint(1,10)}',
        'Category': category,
        'Sub_Category': sub_cat,
        'Product_Name': product,
        'Quantity': quantity,
        'Unit_Price': price,
        'Discount': discount,
        'Sales': sales,
        'Cost': cost,
        'Profit': profit,
        'Season': get_season(order_date.month),
        'Month': order_date.month,
        'Year': order_date.year,
        'Month_Name': order_date.strftime('%B'),
        'Quarter': f'Q{(order_date.month-1)//3+1}',
    })
    order_id += 1

df = pd.DataFrame(rows)
df.to_csv('data/sales_data.csv', index=False)
print(f"Dataset generated: {len(df)} rows, {len(df.columns)} columns")