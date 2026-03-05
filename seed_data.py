from database import get_db_connection, init_db
import sqlite3

VIZAG_LISTINGS = [
    ("Sea-facing 3BHK Apartment", 7500000, "MVP Colony", "Apartment", "9876543210"),
    ("Modern 2BHK Flat", 4500000, "Madhurawada", "Flat", "9876543211"),
    ("Spacious 4BHK Villa", 15000000, "Rushikonda", "Villa", "9876543212"),
    ("Budget 2BHK Flat", 3500000, "Gajuwaka", "Flat", "9876543213"),
    ("Luxurious 3BHK Apartment", 8500000, "Seethammadhara", "Apartment", "9876543214"),
    ("Independent 3BHK House", 9500000, "MVP Colony", "House", "9876543215"),
    ("Premium 2BHK Flat", 5000000, "Madhurawada", "Flat", "9876543216"),
    ("Seaside Penthouse", 12500000, "Rushikonda", "Penthouse", "9876543217"),
    ("Commercial Shop", 4000000, "Gajuwaka", "Shop", "9876543218"),
    ("Modern Villa", 11000000, "Seethammadhara", "Villa", "9876543219"),
    ("Garden View Apartment", 6500000, "MVP Colony", "Apartment", "9876543220"),
    ("Cozy 1BHK Flat", 2500000, "Madhurawada", "Flat", "9876543221"),
    ("Beachfront Villa", 25000000, "Rushikonda", "Villa", "9876543222"),
    ("Plot for Sale", 3000000, "Gajuwaka", "Plot", "9876543223"),
    ("Executive 3BHK Apartment", 8000000, "Seethammadhara", "Apartment", "9876543224")
]

def seed_database():
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for listing in VIZAG_LISTINGS:
            try:
                cursor.execute(
                    "INSERT INTO properties (title, price, area, property_type, contact) VALUES (?, ?, ?, ?, ?)",
                    listing
                )
            except sqlite3.IntegrityError:
                # If the property already exists, skip it
                pass
        conn.commit()
    print("Database seeded with 15 Vizag listings. Duplicate entries were skipped.")

if __name__ == "__main__":
    seed_database()
