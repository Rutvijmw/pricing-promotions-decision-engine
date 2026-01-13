-- Daily KPIs (overall)
CREATE VIEW IF NOT EXISTS vw_kpis_daily AS
SELECT date,
       SUM(units) AS units,
       SUM(revenue_gbp) AS revenue_gbp,
       SUM(gross_profit_gbp) AS gross_profit_gbp,
       AVG(price_gbp) AS avg_price_gbp,
       1.0*SUM(CASE WHEN is_promo=1 THEN revenue_gbp ELSE 0 END) / NULLIF(SUM(revenue_gbp),0) AS promo_revenue_share,
       1.0*SUM(stockout_flag) / NULLIF(COUNT(*),0) AS stockout_rate
FROM fact_sales_daily
GROUP BY 1;

-- Weekly KPIs by category
CREATE VIEW IF NOT EXISTS vw_kpis_weekly_category AS
SELECT substr(date,1,4) || '-W' || printf('%02d', CAST(strftime('%W', date) AS INTEGER)) AS year_week,
       i.category,
       SUM(s.units) AS units,
       SUM(s.revenue_gbp) AS revenue_gbp,
       SUM(s.gross_profit_gbp) AS gross_profit_gbp,
       AVG(s.price_gbp) AS avg_price_gbp,
       SUM(CASE WHEN s.is_promo=1 THEN 1 ELSE 0 END) AS promo_rows
FROM fact_sales_daily s
JOIN dim_item i ON i.item_id = s.item_id
GROUP BY 1,2;

-- Promo performance by discount bucket
CREATE VIEW IF NOT EXISTS vw_promo_performance AS
SELECT i.category,
       CASE
         WHEN discount_depth = 0 THEN '0%'
         WHEN discount_depth <= 0.15 THEN '10-15%'
         WHEN discount_depth <= 0.25 THEN '20-25%'
         ELSE '30%+'
       END AS discount_bucket,
       COUNT(*) AS rows,
       SUM(units) AS units,
       SUM(revenue_gbp) AS revenue_gbp,
       SUM(gross_profit_gbp) AS gross_profit_gbp,
       AVG(price_gbp) AS avg_price_gbp,
       1.0*SUM(stockout_flag)/COUNT(*) AS stockout_rate
FROM fact_sales_daily s
JOIN dim_item i ON i.item_id = s.item_id
GROUP BY 1,2;

-- Data quality checks
CREATE VIEW IF NOT EXISTS vw_data_quality AS
SELECT 'fact_sales_daily' AS table_name,
       COUNT(*) AS row_count,
       SUM(CASE WHEN store_id IS NULL OR item_id IS NULL OR date IS NULL THEN 1 ELSE 0 END) AS null_key_rows,
       SUM(CASE WHEN units < 0 THEN 1 ELSE 0 END) AS negative_units_rows
FROM fact_sales_daily;
