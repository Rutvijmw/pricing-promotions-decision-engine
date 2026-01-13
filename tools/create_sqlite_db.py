from __future__ import annotations
from pathlib import Path
import sqlite3
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
DB = BASE / "data" / "processed" / "pricing_promotions.db"
SQL = BASE / "sql"

def exec_sql(conn: sqlite3.Connection, path: Path) -> None:
    conn.executescript(path.read_text(encoding="utf-8"))

def main():
    DB.parent.mkdir(parents=True, exist_ok=True)
    if DB.exists():
        DB.unlink()

    conn = sqlite3.connect(DB)
    exec_sql(conn, SQL / "01_schema.sql")

    pd.read_csv(RAW / "stores.csv").to_sql("dim_store", conn, if_exists="replace", index=False)
    pd.read_csv(RAW / "items.csv").to_sql("dim_item", conn, if_exists="replace", index=False)
    pd.read_csv(RAW / "dim_date.csv").to_sql("dim_date", conn, if_exists="replace", index=False)

    pd.read_csv(RAW / "sales_daily.csv").to_sql("fact_sales_daily", conn, if_exists="replace", index=False)
    pd.read_csv(RAW / "promotions.csv").to_sql("fact_promotions", conn, if_exists="replace", index=False)

    exec_sql(conn, SQL / "02_views.sql")

    conn.commit()
    conn.close()
    print(f"✅ SQLite database created for Tableau/Power BI: {DB}")

if __name__ == "__main__":
    main()
