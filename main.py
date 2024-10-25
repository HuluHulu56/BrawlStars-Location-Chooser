from capture import capture_packets, stop_event
from geo import get_geo_data, close_reader

# List of available countries with their regions and country codes
available_countries = [
    {"name": "United States (Oregon)", "region": "Oregon", "country_code": "US"},
    {"name": "United States (California)", "region": "California", "country_code": "US"},
    {"name": "United States (Virginia)", "region": "Virginia", "country_code": "US"},
    {"name": "United States (Florida)", "region": "Florida", "country_code": "US"},
    {"name": "United States (Texas)", "region": "Texas", "country_code": "US"},
    {"name": "Japan", "region": "Tokyo", "country_code": "JP"},
    {"name": "Ireland", "region": "Leinster", "country_code": "IE"},
    {"name": "Chile", "region": "Santiago Metropolitan", "country_code": "CL"},
    {"name": "Australia", "region": "New South Wales", "country_code": "AU"},
    {"name": "Hong Kong", "region": "Hong Kong", "country_code": "HK"},
    {"name": "Italy", "region": "Lombardy", "country_code": "IT"},
    {"name": "Peru", "region": "Lima Province", "country_code": "PE"},
    {"name": "Germany", "region": "Hesse", "country_code": "DE"},
    {"name": "Finland", "region": "South Karelia", "country_code": "FI"},
    {"name": "Brazil", "region": "São Paulo", "country_code": "BR"},
    {"name": "Singapore", "region": "Singapore", "country_code": "SG"},
    {"name": "India", "region": "Maharashtra", "country_code": "IN"},
    {"name": "Bahrain", "region": "Southern Governorate", "country_code": "BH"}
]

def choose_country():
    print("Please choose a country from the following list:")
    for i, country in enumerate(available_countries, 1):
        print(f"{i}. {country['name']}")
    while True:
        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            if 1 <= choice <= len(available_countries):
                chosen = available_countries[choice - 1]
                return chosen['country_code'], chosen['region']
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    chosen_country, chosen_region = choose_country()
    print(f"Chosen country code: {chosen_country}")
    print(f"Chosen region: {chosen_region}")

    capture_packets(chosen_country, chosen_region, get_geo_data)

if __name__ == "__main__":
    try:
        main()
    finally:
        close_reader()