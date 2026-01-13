# Dashboard Specs — Pricing & Promotions Cockpit

Build in Tableau or Power BI.

## Global filters
Date range, Store region, Store format, Category, Item, Promo flag, Discount bucket.

## Tab 1 — Executive Overview
KPIs: Revenue, Gross Profit, Units, Promo Revenue Share, Avg Price, Stockout Rate  
Views: KPI strip, weekly trends, category/region contribution.

## Tab 2 — Promotions Performance
Views: Incremental GP by discount bucket, ROI proxy by category, promo mix, stockout vs promo depth.

## Tab 3 — Price Elasticity
Views: Elasticity by category ranking and sensitivity summary.

## Tab 4 — Scenario Planner (parameter-driven)
Inputs: Category/Item + Discount %  
Outputs: expected volume change + gross profit impact (use artifacts outputs as reference tables).

## Tab 5 — Data Quality
Use vw_data_quality to show row counts and basic validation.

## Screenshot names for GitHub
overview.png, promo_performance.png, elasticity.png, scenario_planner.png, data_quality.png
