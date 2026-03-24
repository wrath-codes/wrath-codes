"""Main migration orchestrator: legacy protesto → normalized schema."""

from pathlib import Path

import duckdb

from migrate import DB_PATH
from migrate.schema import run as create_schema
from migrate.reference import run as migrate_reference
from migrate.pessoas import run as migrate_pessoas
from migrate.titulos import run as migrate_titulos
from migrate.operacional import run as migrate_operacional
from migrate.custas import run as migrate_custas


def main() -> None:
    print("=" * 60)
    print("PROTESTO — Migration to v2 schema")
    print("=" * 60)

    if DB_PATH.exists():
        DB_PATH.unlink()
    wal = DB_PATH.with_suffix(".duckdb.wal")
    if wal.exists():
        wal.unlink()

    con = duckdb.connect(str(DB_PATH))

    try:
        create_schema(con)
        migrate_reference(con)
        migrate_pessoas(con)
        migrate_titulos(con)
        migrate_operacional(con)
        migrate_custas(con)

        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        tables = con.execute("""
            SELECT table_name, estimated_size
            FROM duckdb_tables()
            WHERE schema_name = 'main'
            ORDER BY estimated_size DESC, table_name
        """).fetchall()
        total = 0
        for name, size in tables:
            if size > 0:
                print(f"  {name:<30} {size:>10,}")
            total += size
        print(f"  {'─' * 42}")
        print(f"  {'TOTAL':<30} {total:>10,}")
        print(f"\n  Database: {DB_PATH}")
    finally:
        con.close()


if __name__ == "__main__":
    main()
