from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parents[1]
ART = BASE / "artifacts"

promo_path = ART / "promo_uplift_by_category_discount.csv"
elas_path = ART / "price_elasticity_by_category.csv"
top_path  = ART / "top_promo_candidates.csv"

out_path = ART / "RESULTS_INSIGHTS.md"

def safe_float(x):
    try:
        if pd.isna(x):
            return None
        return float(x)
    except Exception:
        return None

def main():
    lines = []
    lines.append("## Results & Insights\n")

    # Elasticity
    if elas_path.exists():
        e = pd.read_csv(elas_path)
        e["price_elasticity"] = pd.to_numeric(e["price_elasticity"], errors="coerce")
        e = e.dropna(subset=["price_elasticity"]).sort_values("price_elasticity")  # most negative first

        most_sensitive = e.iloc[0]
        least_sensitive = e.iloc[-1]

        lines.append("### Price Elasticity (Category-level)\n")
        lines.append(f"- **Most price-sensitive category:** **{most_sensitive['category']}** (elasticity **{most_sensitive['price_elasticity']:.2f}**, R² {most_sensitive.get('r2', np.nan):.2f})")
        lines.append(f"- **Least price-sensitive category:** **{least_sensitive['category']}** (elasticity **{least_sensitive['price_elasticity']:.2f}**, R² {least_sensitive.get('r2', np.nan):.2f})")
        lines.append("\n> Interpretation: elasticity is typically negative; more negative means demand is more sensitive to price changes.\n")

    # Promo uplift / ROI
    if promo_path.exists():
        p = pd.read_csv(promo_path)

        # Make sure numeric cols are numeric
        for col in ["incremental_gp", "incremental_units", "roi_proxy", "discount_cost", "promo_units"]:
            if col in p.columns:
                p[col] = pd.to_numeric(p[col], errors="coerce")

        # Best overall discount bucket (by ROI proxy and incremental GP)
        best_bucket = (
            p.dropna(subset=["roi_proxy"])
             .groupby("discount_bucket", as_index=False)
             .agg(roi_proxy=("roi_proxy","mean"), incremental_gp=("incremental_gp","sum"), promo_units=("promo_units","sum"))
             .sort_values(["roi_proxy","incremental_gp"], ascending=False)
        )

        lines.append("### Promotion Uplift & ROI (Discount Depth)\n")
        if len(best_bucket) > 0:
            bb = best_bucket.iloc[0]
            lines.append(f"- **Best overall discount depth bucket:** **{bb['discount_bucket']}** (avg ROI proxy **{bb['roi_proxy']:.2f}**, total incremental GP **£{bb['incremental_gp']:.0f}**)")

        # Best bucket per category
        best_per_cat = (
            p.dropna(subset=["roi_proxy"])
             .sort_values(["category","roi_proxy","incremental_gp"], ascending=[True, False, False])
             .groupby("category", as_index=False)
             .first()
        )

        lines.append("- **Best discount depth by category (ROI proxy):**")
        for r in best_per_cat.itertuples(index=False):
            lines.append(f"  - {r.category}: **{r.discount_bucket}** (ROI {r.roi_proxy:.2f}, incr GP £{r.incremental_gp:.0f})")

        lines.append("")

    # Top candidates
    if top_path.exists():
        t = pd.read_csv(top_path)
        # Keep it short for README
        cols = [c for c in ["category","discount_bucket","roi_proxy","incremental_gp","promo_units"] if c in t.columns]
        t = t[cols].head(10)
        lines.append("### Top Promotion Candidates\n")
        lines.append("Top 10 category/discount strategies ranked by ROI proxy and incremental GP:\n")
        lines.append(t.to_markdown(index=False))
        lines.append("")

    # Add chart embeds (GitHub)
    lines.append("### Charts\n")
    lines.append("![Incremental GP by Discount](artifacts/chart_incremental_gp_by_discount.png)")
    lines.append("![Elasticity by Category](artifacts/chart_elasticity_by_category.png)")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Wrote: {out_path}")

if __name__ == "__main__":
    main()
