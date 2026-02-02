#!/usr/bin/env python3
"""Fetch all fuel prices and save to JSON."""
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
        timeout=60,
    )
    
    print("Fetching all fuel prices...")
    try:
        prices = client.get_all_pfs_prices()
    except TimeoutError as e:
        print(f"Error: API request timed out - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    print(f"Retrieved {len(prices)} price records")
    
    # Convert to dict format
    data = {
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "total_records": len(prices),
        "prices": [
            {
                "node_id": p.node_id,
                "organisation": p.mft_organisation_name,
                "trading_name": p.trading_name,
                "fuel_prices": [
                    {
                        "fuel_type": fp.fuel_type,
                        "price": fp.price,
                        "last_updated": fp.price_last_updated.isoformat() + "Z" if fp.price_last_updated else None,
                    }
                    for fp in p.fuel_prices
                ],
            }
            for p in prices
        ],
    }
    
    # Save to JSON
    filename = f"fuel_prices_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved to {filename}")
    
    # Print summary stats
    fuel_types = {}
    total_prices = 0
    for p in prices:
        for fp in p.fuel_prices:
            if fp.price:
                fuel_types[fp.fuel_type] = fuel_types.get(fp.fuel_type, 0) + 1
                total_prices += 1
    
    print(f"\nTotal sites with prices: {len(prices)}")
    print(f"Total price records: {total_prices}")
    print("\nPrices by fuel type:")
    for fuel_type, count in sorted(fuel_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {fuel_type}: {count}")

if __name__ == "__main__":
    main()
