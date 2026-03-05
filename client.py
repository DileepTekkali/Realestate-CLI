import sys
from database import search_properties, init_db
from seed_data import seed_database
import os

def display_menu():
    print("\n--- Vizag Real Estate Search ---")
    print("1. Search by Area")
    print("2. Search by Maximum Price")
    print("3. List all Properties")
    print("4. Re-seed Database")
    print("5. Exit")

def main():
    # Initialize DB if it doesn't exist
    if not os.path.exists("real_estate.db"):
        print("Initializing database...")
        seed_database()

    while True:
        display_menu()
        choice = input("\nChoose an option: ")
        
        if choice == '1':
            area = input("Enter area (e.g., MVP Colony, Madhurawada): ")
            results = search_properties(area=area)
        elif choice == '2':
            try:
                max_price = float(input("Enter maximum price (in ₹): "))
                results = search_properties(max_price=max_price)
            except ValueError:
                print("Invalid price.")
                continue
        elif choice == '3':
            results = search_properties()
        elif choice == '4':
            seed_database()
            continue
        elif choice == '5':
            sys.exit()
        else:
            print("Invalid choice.")
            continue

        if not results:
            print("No properties found.")
        else:
            for p in results:
                print(p)

if __name__ == "__main__":
    main()
