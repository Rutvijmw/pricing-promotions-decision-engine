from __future__ import annotations
from pathlib import Path
import sqlite3
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parents[1]
DB = BASE / "data" / "processed" / "pricing_promotions.db"
OUT = BASE / "artifacts"
OUT.mkdir(exist_ok=True)

def main():
    if not DB.exists():
        raise FileNotFoundError(f"Missing DB: {DB}. Run: python tools/create_sqlite_db.py")

    conn = sqlite3.connect(DB)
    sales = pd.read_sql_query(
        '''
        SELECT s.date, s.store_id, s.item_id, s.is_promo, s.discount_depth, s.units, s.revenue_gbp, s.gross_profit_gbp,
               i.category, i.regular_price_gbp, i.unit_cost_gbp
        FROM fact_sales_daily s
        JOIN dim_item i ON i.item_id = s.item_id
        ''',
        conn
    )
    conn.close()

    # Baseline = median non-promo units per store-item (robust baseline)
    baseline = (
        sales[sales["is_promo"] == 0]
        .groupby(["store_id", "item_id"])["units"]
        .median()
        .rename("baseline_units")
        .reset_index()
    )

    df = sales.merge(baseline, on=["store_id", "item_id"], how="left")
    df["baseline_units"] = df["baseline_units"].fillna(df["units"].median())

    df["incr_units"] = np.where(df["is_promo"] == 1, df["units"] - df["baseline_units"], 0.0)
    df["incr_gp_gbp"] = np.where(
        df["is_promo"] == 1,
        df["incr_units"] * (df["regular_price_gbp"] - df["unit_cost_gbp"]),
        0.0
    )

    def bucket(d: float) -> str:
        if d == 0:
            return "0%"
        if d <= 0.15:
            return "10-15%"
        if d <= 0.25:
            return "20-25%"
        return "30%+"

    df["discount_bucket"] = df["discount_depth"].fillna(0).apply(bucket)

    # Discount cost proxy: margin given up on baseline volume
    df["discount_cost_gbp"] = np.where(
        df["is_promo"] == 1,
        df["baseline_units"] * df["discount_depth"].fillna(0) * df["regular_price_gbp"],
        0.0
    )

    summary = (
        df[df["is_promo"] == 1]
        .groupby(["category", "discount_bucket"])
        .agg(
            promo_rows=("units", "size"),
            promo_units=("units", "sum"),
            promo_gross_profit=("gross_profit_gbp", "sum"),
            incremental_units=("incr_units", "sum"),
            incremental_gp=("incr_gp_gbp", "sum"),
            discount_cost=("discount_cost_gbp", "sum"),
        )
        .reset_index()
        .sort_values(["category", "discount_bucket"])
    )
    summary["roi_proxy"] = summary["incremental_gp"] / summary["discount_cost"].replace({0: np.nan})

    summary.to_csv(OUT / "promo_uplift_by_category_discount.csv", index=False)

    top = summary.sort_values(["roi_proxy", "incremental_gp"], ascending=False).head(30)
    top.to_csv(OUT / "top_promo_candidates.csv", index=False)

    print("✅ Saved promo outputs to artifacts/")

if __name__ == "__main__":
    main()
