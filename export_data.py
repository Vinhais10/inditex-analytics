import pandas as pd
from db import run_query

# Exportar brands + sales_by_brand
brands = run_query("SELECT * FROM brands;")
sales = run_query("SELECT * FROM sales_by_brand;")
financials = run_query("SELECT * FROM financials;")
regions = run_query("SELECT * FROM sales_by_region;")

brands.to_csv("brands.csv", index=False)
sales.to_csv("sales_by_brand.csv", index=False)
financials.to_csv("financials.csv", index=False)
regions.to_csv("sales_by_region.csv", index=False)

print("CSVs exportados.")
