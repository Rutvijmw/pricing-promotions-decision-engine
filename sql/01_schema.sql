-- SQLite schema (dimensions + facts)
CREATE TABLE IF NOT EXISTS dim_store (
  store_id TEXT PRIMARY KEY,
  store_region TEXT,
  store_format TEXT
);

CREATE TABLE IF NOT EXISTS dim_item (
  item_id TEXT PRIMARY KEY,
  category TEXT,
  brand_tier TEXT,
  regular_price_gbp REAL,
  unit_cost_gbp REAL
);

CREATE TABLE IF NOT EXISTS dim_date (
  date TEXT PRIMARY KEY,
  year INTEGER,
  month INTEGER,
  year_month TEXT,
  week INTEGER,
  day_name TEXT
);

CREATE TABLE IF NOT EXISTS fact_sales_daily (
  date TEXT,
  store_id TEXT,
  item_id TEXT,
  price_gbp REAL,
  is_promo INTEGER,
  discount_depth REAL,
  promo_type TEXT,
  units INTEGER,
  revenue_gbp REAL,
  gross_profit_gbp REAL,
  stockout_flag INTEGER
);

CREATE TABLE IF NOT EXISTS fact_promotions (
  store_id TEXT,
  item_id TEXT,
  promo_start TEXT,
  promo_end TEXT,
  promo_type TEXT,
  discount_depth REAL
);
