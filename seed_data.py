"""Top-level seed script for inserting mock real estate listings."""

from real_estate_cli.seed_data import seed_database


if __name__ == "__main__":
    inserted, skipped = seed_database(reset=False)
    print(
        f"Seed complete. Inserted {inserted} new listings, "
        f"skipped {skipped} duplicates."
    )
