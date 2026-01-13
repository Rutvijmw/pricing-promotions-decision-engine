from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "artifacts"
OUT.mkdir(exist_ok=True)

def _savefig(name: str):
    plt.tight_layout()
    plt.savefig(OUT / name, dpi=200)
    plt.close()

def main():
    f1 = OUT / "promo_uplift_by_category_discount.csv"
    if f1.exists():
        df = pd.read_csv(f1)
        g = df.groupby("discount_bucket")["incremental_gp"].sum()
        plt.figure()
        g.plot(kind="bar")
        plt.title("Incremental Gross Profit by Discount Depth")
        plt.xlabel("Discount Depth")
        plt.ylabel("Incremental Gross Profit (GBP)")
        _savefig("chart_incremental_gp_by_discount.png")

    f2 = OUT / "price_elasticity_by_category.csv"
    if f2.exists():
        e = pd.read_csv(f2).set_index("category")["price_elasticity"].sort_values()
        plt.figure()
        e.plot(kind="bar")
        plt.title("Estimated Price Elasticity by Category (log-log)")
        plt.xlabel("Category")
        plt.ylabel("Elasticity (negative = price sensitive)")
        _savefig("chart_elasticity_by_category.png")

    print("✅ Charts saved to artifacts/")

if __name__ == "__main__":
    main()
