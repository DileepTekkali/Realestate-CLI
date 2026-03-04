"""Data model and query helpers for properties."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .database import get_connection


@dataclass(slots=True)
class Property:
    title: str
    area: str
    property_type: str
    bedrooms: int
    bathrooms: int
    sqft: int
    price: int
    listing_type: str
    description: str = ""
    id: int | None = None


def add_property(property_data: Property) -> int:
    """Insert a property into the database and return its new id."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO properties (
                title, area, property_type, bedrooms, bathrooms, sqft,
                price, listing_type, description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                property_data.title,
                property_data.area,
                property_data.property_type,
                property_data.bedrooms,
                property_data.bathrooms,
                property_data.sqft,
                property_data.price,
                property_data.listing_type,
                property_data.description,
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def bulk_add_properties(properties: Iterable[Property]) -> int:
    """Insert multiple properties and return count inserted."""
    rows = [
        (
            p.title,
            p.area,
            p.property_type,
            p.bedrooms,
            p.bathrooms,
            p.sqft,
            p.price,
            p.listing_type,
            p.description,
        )
        for p in properties
    ]
    if not rows:
        return 0

    with get_connection() as conn:
        conn.executemany(
            """
            INSERT INTO properties (
                title, area, property_type, bedrooms, bathrooms, sqft,
                price, listing_type, description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()
    return len(rows)


def list_properties(limit: int = 50) -> list[dict]:
    """Return recent properties up to the requested limit."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT id, title, area, property_type, bedrooms, bathrooms, sqft, price, listing_type
            FROM properties
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]


def search_properties(
    area: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    listing_type: str | None = None,
    bedrooms: int | None = None,
) -> list[dict]:
    """Search properties by optional filters."""
    conditions: list[str] = []
    params: list[object] = []

    if area:
        conditions.append("area = ?")
        params.append(area)
    if min_price is not None:
        conditions.append("price >= ?")
        params.append(min_price)
    if max_price is not None:
        conditions.append("price <= ?")
        params.append(max_price)
    if listing_type:
        conditions.append("listing_type = ?")
        params.append(listing_type)
    if bedrooms is not None:
        conditions.append("bedrooms = ?")
        params.append(bedrooms)

    query = """
        SELECT id, title, area, property_type, bedrooms, bathrooms, sqft, price, listing_type
        FROM properties
    """
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY price ASC;"

    with get_connection() as conn:
        cursor = conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def delete_all_properties() -> None:
    """Clear all property records (used by seed routine)."""
    with get_connection() as conn:
        conn.execute("DELETE FROM properties;")
        conn.commit()
