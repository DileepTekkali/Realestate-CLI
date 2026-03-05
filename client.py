import sys
import os
from database import search_properties
from seed_data import seed_database

def clear_screen():
    """Clears the terminal screen for a cleaner UI."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Prints a styled header for the CLI."""
    print("=" * 80)
    print(" " * 25 + "🏠 VIZAG REAL ESTATE SEARCH")
    print("=" * 80)

def display_results(results, area):
    """Formats and displays the search results in a pretty, tabular format."""
    count = len(results)
    print(f"\n🔍 Found {count} result(s) for area: '{area}'")
    
    if count == 0:
        print(f"\n   [!] No properties matching '{area}' were found.")
        print("   💡 Try searching for: MVP Colony, Madhurawada, Rushikonda, Gajuwaka, or Seethammadhara.")
    else:
        # Table Header
        header = f"{'ID':<4} | {'Title':<30} | {'Type':<12} | {'Price (₹)':<15} | {'Contact'}"
        print("\n" + header)
        print("-" * 85)
        
        for p in results:
            # Truncate title if too long
            title = (p.title[:27] + '...') if len(p.title) > 30 else p.title
            # Format price with Indian numbering system style (approx)
            formatted_price = f"{int(p.price):,}"
            
            print(f"{p.id:<4} | {title:<30} | {p.property_type:<12} | {formatted_price:<15} | {p.contact}")
        
    print("-" * 85)

def main():
    # Ensure database exists
    if not os.path.exists("real_estate.db"):
        print("Initializing database...")
        seed_database()
        clear_screen()

    while True:
        print_header()
        print("\nAvailable Search Options:")
        print(" [1] Search by Area Name")
        print(" [2] Exit Program")
        
        choice = input("\nSelect an option (1-2): ").strip()

        if choice == '2':
            print("\nThank you for using Vizag Real Estate Search. Goodbye! 👋")
            break
        elif choice == '1':
            area_input = input("\nEnter the area name to search: ").strip()
            
            if not area_input:
                print("\n[!] Error: Area name cannot be empty.")
            else:
                results = search_properties(area=area_input)
                display_results(results, area_input)
            
            # Wait for user before clearing for next search
            input("\nPress Enter to return to the main menu...")
            clear_screen()
        else:
            print("\n[!] Invalid selection. Please choose 1 or 2.")
            input("\nPress Enter to try again...")
            clear_screen()

if __name__ == "__main__":
    try:
        clear_screen()
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user. Goodbye!")
        sys.exit(0)
