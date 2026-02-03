#!/usr/bin/env python3
"""Search for fuel stations by location."""
import os
import sys
from ukfuelfinder import FuelFinderClient

def main():
    if len(sys.argv) < 3:
        print("Usage: python location_search.py <latitude> <longitude> [radius_km]")
        print("Example: python location_search.py 51.5074 -0.1278 5")
        sys.exit(1)
    
    search_lat = float(sys.argv[1])
    search_lon = float(sys.argv[2])
    radius_km = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
    
    client = FuelFinderClient(
        client_id=os.getenv("FUEL_FINDER_CLIENT_ID"),
        client_secret=os.getenv("FUEL_FINDER_CLIENT_SECRET"),
        timeout=60,
    )
    
    print(f"Searching for stations within {radius_km}km of ({search_lat}, {search_lon})...")
    
    nearby = client.search_by_location(search_lat, search_lon, radius_km)
    
    print(f"\nFound {len(nearby)} stations within {radius_km}km:\n")
    
    for distance, site in nearby:
        print(f"{distance:.2f}km - {site.trading_name}")
        print(f"  {site.brand_name or 'No brand'}")
        print(f"  {site.location.address_line_1}, {site.location.postcode}")
        if site.fuel_types:
            print(f"  Fuel types: {', '.join(site.fuel_types)}")
        if site.public_phone_number:
            print(f"  Phone: {site.public_phone_number}")
        print()

if __name__ == "__main__":
    main()
