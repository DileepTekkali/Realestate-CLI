"""Command-line client for the real estate search project."""

from __future__ import annotations

import argparse

from .database import init_database
from .models import list_properties, search_properties
from .seed_data import seed_database


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="realestate-cli",
        description="SQLite-backed real estate search for Vizag properties.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init-db", help="Create SQLite database and properties table.")

    seed_parser = subparsers.add_parser("seed", help="Seed database with sample Vizag properties.")
    seed_parser.add_argument(
        "--no-reset",
        action="store_true",
        help="Do not delete existing records before inserting sample data.",
    )

    list_parser = subparsers.add_parser("list", help="List latest properties.")
    list_parser.add_argument("--limit", type=int, default=20, help="Maximum rows to display.")

    search_parser = subparsers.add_parser("search", help="Search properties by filters.")
    search_parser.add_argument("--area", type=str, help="Area name (e.g. MVP Colony).")
    search_parser.add_argument("--min-price", type=int, help="Minimum price.")
    search_parser.add_argument("--max-price", type=int, help="Maximum price.")
    search_parser.add_argument(
        "--listing-type",
        choices=["sale", "rent"],
        help="Filter by listing type.",
    )
    search_parser.add_argument("--bedrooms", type=int, help="Number of bedrooms.")

    return parser


def _print_rows(rows: list[dict]) -> None:
    if not rows:
        print("No properties found.")
        return

    for row in rows:
        print(
            f"[{row['id']}] {row['title']} | {row['area']} | "
            f"{row['property_type']} | {row['bedrooms']}BHK | "
            f"{row['sqft']} sqft | ₹{row['price']} | {row['listing_type']}"
        )


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "init-db":
        init_database()
        print("Database initialized and properties table is ready.")
        return

    if args.command == "seed":
        inserted, skipped = seed_database(reset=not args.no_reset)
        print(
            f"Seed complete. Inserted {inserted} properties, "
            f"skipped {skipped} duplicates."
        )
        return

    if args.command == "list":
        _print_rows(list_properties(limit=args.limit))
        return

    if args.command == "search":
        _print_rows(
            search_properties(
                area=args.area,
                min_price=args.min_price,
                max_price=args.max_price,
                listing_type=args.listing_type,
                bedrooms=args.bedrooms,
            )
        )


if __name__ == "__main__":
    main()
