"""Insert 15 mock Vizag property listings into SQLite, skipping duplicates."""

from __future__ import annotations

import sqlite3

try:
    from .database import get_connection, init_database
except ImportError:  # Allows running as: python real_estate_cli/seed_data.py
    from database import get_connection, init_database

MOCK_LISTINGS = [
    {
        "title": "2BHK Apartment Near Beach Road",
        "price": 6200000,
        "area": "MVP Colony",
        "property_type": "Apartment",
        "contact": "9000010001",
    },
    {
        "title": "3BHK Family Flat",
        "price": 8800000,
        "area": "MVP Colony",
        "property_type": "Apartment",
        "contact": "9000010002",
    },
    {
        "title": "Independent Duplex Home",
        "price": 14500000,
        "area": "MVP Colony",
        "property_type": "House",
        "contact": "9000010003",
    },
    {
        "title": "Gated 2BHK Residency",
        "price": 5600000,
        "area": "Madhurawada",
        "property_type": "Apartment",
        "contact": "9000010004",
    },
    {
        "title": "Luxury 4BHK Villa",
        "price": 18200000,
        "area": "Madhurawada",
        "property_type": "Villa",
        "contact": "9000010005",
    },
    {
        "title": "Budget 1BHK Rental Unit",
        "price": 14000,
        "area": "Madhurawada",
        "property_type": "Apartment",
        "contact": "9000010006",
    },
    {
        "title": "Industrial Area Staff Quarters",
        "price": 22000,
        "area": "Gajuwaka",
        "property_type": "Apartment",
        "contact": "9000010007",
    },
    {
        "title": "Corner Plot Independent House",
        "price": 7600000,
        "area": "Gajuwaka",
        "property_type": "House",
        "contact": "9000010008",
    },
    {
        "title": "Compact 2BHK Home",
        "price": 5100000,
        "area": "Gajuwaka",
        "property_type": "Apartment",
        "contact": "9000010009",
    },
    {
        "title": "Sea View Premium Studio",
        "price": 19000,
        "area": "Rushikonda",
        "property_type": "Studio",
        "contact": "9000010010",
    },
    {
        "title": "Beachside 3BHK Penthouse",
        "price": 13200000,
        "area": "Rushikonda",
        "property_type": "Penthouse",
        "contact": "9000010011",
    },
    {
        "title": "Serviced 2BHK Flat",
        "price": 30000,
        "area": "Rushikonda",
        "property_type": "Apartment",
        "contact": "9000010012",
    },
    {
        "title": "Classic 3BHK Apartment",
        "price": 9700000,
        "area": "Seethammadhara",
        "property_type": "Apartment",
        "contact": "9000010013",
    },
    {
        "title": "Renovated 2BHK Unit",
        "price": 6800000,
        "area": "Seethammadhara",
        "property_type": "Apartment",
        "contact": "9000010014",
    },
    {
        "title": "Compact Family House",
        "price": 8300000,
        "area": "Seethammadhara",
        "property_type": "House",
        "contact": "9000010015",
    },
]


def _table_columns(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute("PRAGMA table_info(properties);").fetchall()
    return {str(row["name"]) for row in rows}


def _ensure_contact_column(conn: sqlite3.Connection) -> None:
    columns = _table_columns(conn)
    if "contact" not in columns:
        conn.execute("ALTER TABLE properties ADD COLUMN contact TEXT;")
        conn.commit()


def _listing_exists(conn: sqlite3.Connection, listing: dict[str, str | int]) -> bool:
    row = conn.execute(
        """
        SELECT 1
        FROM properties
        WHERE title = ? AND price = ? AND area = ? AND property_type = ? AND contact = ?
        LIMIT 1;
        """,
        (
            listing["title"],
            listing["price"],
            listing["area"],
            listing["property_type"],
            listing["contact"],
        ),
    ).fetchone()
    return row is not None


def _build_insert_payload(
    listing: dict[str, str | int], columns: set[str]
) -> tuple[list[str], list[str | int]]:
    payload: dict[str, str | int] = {
        "title": listing["title"],
        "price": listing["price"],
        "area": listing["area"],
        "property_type": listing["property_type"],
        "contact": listing["contact"],
    }

    # Backward compatibility for older schema versions in this project.
    fallbacks = {
        "bedrooms": 2,
        "bathrooms": 2,
        "sqft": 1200,
        "listing_type": "sale",
        "description": "Seeded mock listing",
    }
    for column_name, default_value in fallbacks.items():
        if column_name in columns:
            payload[column_name] = default_value

    insert_columns = list(payload.keys())
    insert_values = [payload[column] for column in insert_columns]
    return insert_columns, insert_values


def seed_database(reset: bool = False) -> tuple[int, int]:
    """Insert 15 listings. Returns (inserted_count, skipped_duplicates_count)."""
    init_database()
    inserted = 0
    skipped = 0

    with get_connection() as conn:
        _ensure_contact_column(conn)
        if reset:
            conn.execute("DELETE FROM properties;")
            conn.commit()
        columns = _table_columns(conn)

        for listing in MOCK_LISTINGS:
            if _listing_exists(conn, listing):
                skipped += 1
                continue

            insert_columns, insert_values = _build_insert_payload(listing, columns)
            placeholders = ", ".join(["?"] * len(insert_columns))
            column_csv = ", ".join(insert_columns)
            conn.execute(
                f"INSERT INTO properties ({column_csv}) VALUES ({placeholders});",
                insert_values,
            )
            inserted += 1

        conn.commit()

    return inserted, skipped


if __name__ == "__main__":
    inserted_count, skipped_count = seed_database()
    print(
        f"Seed complete. Inserted {inserted_count} new listings, "
        f"skipped {skipped_count} duplicates."
    )
