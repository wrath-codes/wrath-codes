from pathlib import Path

import duckdb
import polars as pl
from klaw_dbase import read_dbase

SOURCE_DIR = Path(r"C:\Users\user\DBF_PROTESTO\PROTESTO")
OUTPUT_DIR = Path(r"C:\Users\user\projects\protesto_out\parquet")
DB_PATH = Path(r"C:\Users\user\projects\protesto_out\protesto.duckdb")

SKIP_PREFIXES = ("BACK", "OLD_", "OLD__", "BKP")
SKIP_CONTAINS = ("OLD",)


def is_backup(name: str) -> bool:
    upper = name.upper()
    if any(upper.startswith(p) for p in SKIP_PREFIXES):
        return True
    if upper.startswith("OLD_") or upper.startswith("OLD__"):
        return True
    if "_OLD" in upper or "OLD_" in upper:
        return True
    return False


def export_all_dbf_to_parquet() -> list[tuple[str, Path]]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    exported: list[tuple[str, Path]] = []
    skipped: list[str] = []

    dbf_files = sorted(SOURCE_DIR.glob("*.dbf"), key=lambda p: p.name.upper())
    dbf_files += sorted(SOURCE_DIR.glob("*.DBF"), key=lambda p: p.name.upper())
    seen = set()
    unique_dbf = []
    for f in dbf_files:
        if f.name.upper() not in seen:
            seen.add(f.name.upper())
            unique_dbf.append(f)

    print(f"Found {len(unique_dbf)} unique DBF files in root directory\n")

    for dbf_path in unique_dbf:
        stem = dbf_path.stem
        table_name = stem.lower().replace("-", "_").replace(" ", "_")

        if is_backup(stem):
            skipped.append(stem)
            continue

        parquet_path = OUTPUT_DIR / f"{table_name}.parquet"
        try:
            df = read_dbase(str(dbf_path))
            df.write_parquet(parquet_path)
            exported.append((table_name, parquet_path))
            print(f"  OK    {stem:<20} -> {table_name}.parquet  ({df.shape[0]:>7,} rows x {df.shape[1]:>3} cols)")
        except Exception as e:
            print(f"  ERR   {stem:<20} {e}")

    print(f"\nSkipped {len(skipped)} backup files: {', '.join(skipped)}")
    return exported


def build_duckdb(exported: list[tuple[str, Path]]) -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    wal = DB_PATH.with_suffix(".duckdb.wal")
    if wal.exists():
        wal.unlink()

    con = duckdb.connect(str(DB_PATH))
    for table_name, parquet_path in exported:
        posix = parquet_path.as_posix()
        con.execute(f"CREATE TABLE \"{table_name}\" AS SELECT * FROM read_parquet('{posix}')")

    tables = con.execute("SELECT table_name, estimated_size FROM duckdb_tables() ORDER BY table_name").fetchall()
    print(f"\nDuckDB: {DB_PATH}")
    print(f"{'Table':<25} {'Est. Rows':>12}")
    print("-" * 40)
    for name, size in tables:
        print(f"  {name:<23} {size:>10,}")

    con.close()


def main():
    print("=" * 70)
    print("PROTESTO SYSTEM - Full DBF Export")
    print("=" * 70)
    print(f"Source: {SOURCE_DIR}")
    print(f"Output: {OUTPUT_DIR}\n")

    exported = export_all_dbf_to_parquet()

    if exported:
        print(f"\n{'=' * 70}")
        print(f"Building DuckDB with {len(exported)} tables...")
        print("=" * 70)
        build_duckdb(exported)

    print(f"\nDone! {len(exported)} tables exported.")


if __name__ == "__main__":
    main()
