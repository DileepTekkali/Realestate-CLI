"""SQLite database utilities for the real estate CLI."""

from __future__ import annotations

import sqlite3
from pathlib import Path

# Database file lives in project_root/data/real_estate.db
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "real_estate.db"


def get_connection(db_path: Path | str = DB_PATH) -> sqlite3.Connection:
    """Return a SQLite connection with row access by column name."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def create_properties_table(conn: sqlite3.Connection) -> None:
    """Create the properties table if it does not already exist."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            area TEXT NOT NULL,
            property_type TEXT NOT NULL,
            bedrooms INTEGER NOT NULL,
            bathrooms INTEGER NOT NULL,
            sqft INTEGER NOT NULL,
            price INTEGER NOT NULL,
            listing_type TEXT NOT NULL CHECK(listing_type IN ('sale', 'rent')),
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()


def init_database(db_path: Path | str = DB_PATH) -> None:
    """Initialize the SQLite database and create required tables."""
    with get_connection(db_path) as conn:
        create_properties_table(conn)
