# Pricing & Promotions Decision Engine (SQL + Python + Dashboard)

Portfolio project aligned to **Sainsbury’s Analyst – Pricing & Promotions**: end-to-end analysis with ETL, SQL, statistical models, and dashboard specs.

## What’s included
- Synthetic retail dataset: stores, items, promotions, daily sales with price & margin
- SQLite data mart + SQL views (KPIs, promo performance, data quality)
- Python analyses:
  - Promotion uplift + ROI proxy (incremental units / incremental GP)
  - Price elasticity by category (log-log regression)
- Charts saved to `/artifacts` for quick sharing
- Dashboard specs + KPI dictionary + stakeholder story

## Quickstart (Windows)
```bash
pip install -r requirements.txt
python run_all.py
```

### Outputs
- `data/processed/pricing_promotions.db` (connect Tableau/Power BI to this)
- `artifacts/` (CSV outputs + PNG charts)

## Tableau / Power BI
Connect to: `data/processed/pricing_promotions.db`  
Use views in `sql/02_views.sql` and artifacts outputs as reference tables.  
Dashboard spec: `docs/dashboard_specs.md`

## ATS resume bullets
- Built an end-to-end pricing & promotions analytics solution using SQL + Python, from ETL to stakeholder-ready insights
- Developed a SQL data mart and automated KPI reporting via reusable views to reduce manual reporting
- Quantified promotion uplift and ROI by discount depth and category to identify high-impact promo strategies
- Estimated price elasticity using regression modelling to support strategic pricing decisions and scenario planning
- Produced a dashboard spec and storytelling pack to translate complex analysis into clear commercial recommendations
