# Sales Analytics Dashboard
## Project Overview

The dashboard helps users:
- Explore sales and profit across years, regions, seasons, and product categories
- View summary KPIs such as total sales, total profit, total orders, average margin, and top region
- Analyze monthly trends and seasonal performance
- Compare regional sales distribution
- Browse a product catalog-style view with pricing, ratings, discounts, and badges

## Features

- Interactive filters for year, region, season, and category
- Visual analytics with Plotly and Matplotlib
- KPI cards for quick business insights
- Sales trend and seasonal analysis
- Region-wise and category-wise performance views
- Product catalog section with styled product cards

## Project Structure

- dashboard/app.py - Main Streamlit dashboard application
- src/data_preprocessing.py - Data cleaning, feature engineering, and chart generation
- src/product_catalog.py - Product catalog metadata generation
- data/ - Input and cleaned datasets
- reports/ - Generated charts and analysis images
- Sales_Analytics_Dashboard_Presentation.pptx - Presentation file for showcasing the project

## Setup Instructions

1. Create and activate a virtual environment
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies
   ```bash
   pip install streamlit pandas numpy plotly matplotlib seaborn
   ```

3. Run the preprocessing script (optional but recommended)
   ```bash
   python src/data_preprocessing.py
   ```

4. Start the dashboard
   ```bash
   streamlit run dashboard/app.py
   ```

## Data Files

The project uses the following data files:
- data/sales_data.csv - Raw sales dataset
- data/cleaned_sales_data.csv - Cleaned and processed dataset used by the dashboard

## Generated Outputs

Running the preprocessing pipeline creates charts in the reports folder, including:
- top_products.png
- season_analysis.png
- region_analysis.png
- monthly_trend.png
- heatmap.png
- profit_margin.png
- yoy_comparison.png
- correlation.png

These outputs can be used in reports, presentations, or academic submissions.

## What to Present

For your presentation, you can showcase:
1. Dashboard overview and user filters
2. Sales and profit KPI summary
3. Seasonal and monthly sales trends
4. Region-wise sales analysis
5. Product catalog and top-performing products
6. Generated charts from the reports folder

## Sample Presentation Flow

- Introduction to the project objective
- Dataset description and preprocessing steps
- Dashboard walkthrough
- Key insights from the analysis
- Conclusion and business value

## Notes

The dashboard is built for demonstration and academic use. It can be extended further with features like forecasting, customer segmentation, and live database integration.
