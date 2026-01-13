from __future__ import annotations
import subprocess, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent

def _run(cmd):
    print("\n>>>", " ".join(cmd))
    subprocess.check_call(cmd, cwd=BASE)

def main():
    _run([sys.executable, "tools/create_sqlite_db.py"])
    _run([sys.executable, "src/analysis_promo_uplift.py"])
    _run([sys.executable, "src/analysis_elasticity.py"])
    _run([sys.executable, "src/create_charts.py"])
    print("\nDONE ✅ Outputs are in /artifacts and the DB is in /data/processed")

if __name__ == "__main__":
    main()
