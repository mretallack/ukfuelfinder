#!/usr/bin/env python3
"""Fetch all forecourt sites and save to JSON."""
import json
import os
import sys
from datetime import datetime
from ukfuelfinder import FuelFinderClient
from ukfuelfinder.exceptions import TimeoutError

def main():
    client = FuelFinderClient(
        client_id=os.getenv("FUEL_FINDER_CLIENT_ID"),
        client_secret=os.getenv("FUEL_FINDER_CLIENT_SECRET"),
        timeout=120,  # 2 minute timeout for slow API
    )
    
    print("Fetching all forecourt sites (this may take a while)...")
    try:
        sites = client.get_all_pfs_info()
    except TimeoutError as e:
        print(f"Error: API request timed out - {e}")
        print("The Fuel Finder API is experiencing performance issues.")
        print("Try using fetch_fuel_prices.py instead, which uses a faster endpoint.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        print("The Fuel Finder API may be under maintenance.")
        sys.exit(1)
    
    print(f"Retrieved {len(sites)} sites")
    
    # Convert to dict format
    data = {
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "total_sites": len(sites),
        "sites": [
            {
                "node_id": site.node_id,
                "trading_name": site.trading_name,
                "organisation": site.mft_organisation_name,
                "brand": site.brand_name,
                "phone": site.public_phone_number,
                "location": {
                    "latitude": site.location.latitude,
                    "longitude": site.location.longitude,
                    "address_line_1": site.location.address_line_1,
                    "address_line_2": site.location.address_line_2,
                    "city": site.location.city,
                    "county": site.location.county,
                    "postcode": site.location.postcode,
                    "country": site.location.country,
                },
                "is_motorway": site.is_motorway_service_station,
                "is_supermarket": site.is_supermarket_service_station,
                "fuel_types": site.fuel_types,
                "amenities": site.amenities,
            }
            for site in sites
        ],
    }
    
    # Save to JSON
    filename = f"forecourt_sites_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved to {filename}")
    
    # Print summary stats
    brands = {}
    for site in sites:
        brand = site.brand_name or "Unknown"
        brands[brand] = brands.get(brand, 0) + 1
    
    print("\nTop 10 brands by site count:")
    for brand, count in sorted(brands.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {brand}: {count}")

if __name__ == "__main__":
    main()
