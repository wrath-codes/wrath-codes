"""Migration package for protesto system re-architecture."""

from pathlib import Path

PARQUET_DIR = Path(r"C:\Users\user\projects\protesto_out\parquet")
DB_PATH = Path(r"C:\Users\user\projects\protesto_out\protesto_v2.duckdb")


def pq(name: str) -> str:
    """Return posix path to a parquet file."""
    return (PARQUET_DIR / f"{name}.parquet").as_posix()


def step(con, label: str, sql: str) -> int:
    """Execute SQL and print row count for the target table."""
    con.execute(sql)
    table = label.strip().split()[0].lower()
    try:
        count = con.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
    except Exception:
        count = -1
    print(f"  {label:<45} {count:>8,} rows")
    return count
