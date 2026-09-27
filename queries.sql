-- ============================================================
-- Inditex Analytics - SQL Queries
-- All queries used in the project, commented
-- ============================================================

-- 1. Financial report for a given year
SELECT year, revenue_millions, net_income_millions,
       gross_margin_pct, stores_count, countries_count
FROM financials
WHERE year = 2025;

-- 2. Sales by brand (JOIN)
SELECT b.brand_name, s.sales_millions, s.growth_pct
FROM sales_by_brand s
JOIN brands b ON s.brand_id = b.brand_id
ORDER BY s.sales_millions DESC;

-- 3. Percentage of total (window function)
SELECT b.brand_name,
       s.sales_millions,
       ROUND(s.sales_millions * 100.0 / SUM(s.sales_millions) OVER (), 2) AS pct_of_total
FROM sales_by_brand s
JOIN brands b ON s.brand_id = b.brand_id
ORDER BY s.sales_millions DESC;

-- 4. Growth ranking (RANK window function)
SELECT b.brand_name,
       s.growth_pct,
       RANK() OVER (ORDER BY s.growth_pct DESC) AS growth_rank
FROM sales_by_brand s
JOIN brands b ON s.brand_id = b.brand_id
ORDER BY growth_rank;

-- 5. ABC analysis (cumulative SUM window function)
SELECT b.brand_name,
       s.sales_millions,
       SUM(s.sales_millions) OVER (ORDER BY s.sales_millions DESC) AS cumulative_sales,
       ROUND(
           SUM(s.sales_millions) OVER (ORDER BY s.sales_millions DESC)
           * 100.0 / SUM(s.sales_millions) OVER (), 2
       ) AS cumulative_pct
FROM sales_by_brand s
JOIN brands b ON s.brand_id = b.brand_id
ORDER BY s.sales_millions DESC;

-- 6. Revenue evolution with YoY growth (LAG window function)
SELECT year,
       revenue_millions,
       LAG(revenue_millions) OVER (ORDER BY year) AS prev_year,
       ROUND(
           (revenue_millions - LAG(revenue_millions) OVER (ORDER BY year))
           * 100.0 / LAG(revenue_millions) OVER (ORDER BY year), 2
       ) AS yoy_growth_pct
FROM financials
ORDER BY year;

-- 7. Revenue per store (efficiency)
SELECT year,
       stores_count,
       ROUND(revenue_millions / stores_count, 2) AS revenue_per_store_millions
FROM financials
ORDER BY year;

-- 8. Top 3 fastest-growing brands with market share (CTE + window function)
WITH latest AS (
    SELECT brand_id, sales_millions, growth_pct
    FROM sales_by_brand
    WHERE year = (SELECT MAX(year) FROM sales_by_brand)
)
SELECT b.brand_name,
       l.growth_pct,
       ROUND((l.sales_millions / SUM(l.sales_millions) OVER ()) * 100, 2) AS sales_share_pct
FROM latest l
JOIN brands b ON b.brand_id = l.brand_id
ORDER BY l.growth_pct DESC
LIMIT 3;

-- 9. Query log (most recent 10)
SELECT id, LEFT(question, 60) AS question,
       success, duration_ms, created_at
FROM query_log
ORDER BY id DESC
LIMIT 10;

-- 10. Average query duration (performance)
SELECT
    COUNT(*) AS total_queries,
    AVG(duration_ms)::INT AS avg_duration_ms,
    MAX(duration_ms) AS max_duration_ms,
    SUM(CASE WHEN success THEN 1 ELSE 0 END) AS successful_queries
FROM query_log;