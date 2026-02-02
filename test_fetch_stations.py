#!/usr/bin/env python3.11
"""
Fetch and display current fuel stations
"""
import os
from dotenv import load_dotenv
from ukfuelfinder import FuelFinderClient

# Load credentials
load_dotenv()

# Initialize client
client = FuelFinderClient(
    client_id=os.getenv("FUEL_FINDER_CLIENT_ID"),
    client_secret=os.getenv("FUEL_FINDER_CLIENT_SECRET"),
    environment="production"
)

print("Fetching fuel stations...")
print("=" * 80)

try:
    # Get first batch of prices
    pfs_list = client.get_all_pfs_prices(batch_number=1)
    
    print(f"\nFound {len(pfs_list)} stations in batch 1\n")
    
    # Display first 10 stations
    for i, pfs in enumerate(pfs_list[:10], 1):
        print(f"{i}. {pfs.trading_name}")
        print(f"   Organization: {pfs.mft_organisation_name}")
        print(f"   Node ID: {pfs.node_id}")
        print(f"   Phone: {pfs.public_phone_number or 'N/A'}")
        print(f"   Fuel Prices:")
        for price in pfs.fuel_prices:
            print(f"     - {price.fuel_type}: £{price.price/100:.2f}")
        print()
    
    if len(pfs_list) > 10:
        print(f"... and {len(pfs_list) - 10} more stations")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
