from db import run_query

df = run_query("SELECT * FROM brands ORDER BY brand_id;")
print(df)
