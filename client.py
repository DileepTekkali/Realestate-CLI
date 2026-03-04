"""Interactive CLI client to search properties by area."""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "real_estate.db"


def fetch_properties_by_area(area: str) -> list[sqlite3.Row]:
    """Return all properties for a given area (case-insensitive)."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            """
            SELECT title, price, area, property_type, contact
            FROM properties
            WHERE area = ? COLLATE NOCASE
            ORDER BY price ASC;
            """,
            (area,),
        )
        return cursor.fetchall()


def print_properties(area: str, rows: list[sqlite3.Row]) -> None:
    """Render query results in a readable format."""
    if not rows:
        print(f"No properties found in '{area}'.")
        return

    print(f"\nProperties available in {area} ({len(rows)} found):\n")
    for idx, row in enumerate(rows, start=1):
        contact = row["contact"] if row["contact"] else "N/A"
        print(f"{idx}. {row['title']}")
        print(f"   Type    : {row['property_type']}")
        print(f"   Price   : Rs {row['price']:,}")
        print(f"   Contact : {contact}\n")


def main() -> None:
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}. Run seed_data.py first.")
        return

    area = input("Enter area name (e.g., MVP Colony): ").strip()
    if not area:
        print("Area name cannot be empty.")
        return

    results = fetch_properties_by_area(area)
    print_properties(area, results)


if __name__ == "__main__":
    main()
