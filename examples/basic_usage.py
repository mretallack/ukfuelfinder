"""
Basic usage example for UK Fuel Finder API (New API - Feb 2025)

This example demonstrates using the new API without backward compatibility.
The response objects no longer have 'success' and 'message' fields.
"""
from ukfuelfinder import FuelFinderClient

# Initialize client without backward compatibility
client = FuelFinderClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    environment="production",
    backward_compatible=False  # Use new API format
)

# Get all PFS with fuel prices
print("Fetching all PFS with fuel prices...")
pfs_list = client.get_all_pfs_prices()
print(f"Found {len(pfs_list)} petrol filling stations\n")

# Display first few stations
for pfs in pfs_list[:5]:
    print(f"{pfs.trading_name} ({pfs.mft_organisation_name})")
    print(f"Node ID: {pfs.node_id}")
    for price in pfs.fuel_prices:
        print(f"  {price.fuel_type}: £{price.price/100:.2f}")
        # New field: price_change_effective_timestamp
        if hasattr(price, 'price_change_effective_timestamp') and price.price_change_effective_timestamp:
            print(f"    Effective: {price.price_change_effective_timestamp}")
    print()

# Get all unleaded prices
print("\nFetching unleaded prices...")
unleaded_prices = client.get_prices_by_fuel_type("unleaded")
print(f"Found {len(unleaded_prices)} unleaded prices")

# Get forecourt information
print("\nFetching forecourt information...")
forecourts = client.get_all_pfs_info(batch_number=1)
print(f"Found {len(forecourts)} forecourts in first batch")

# Display cache statistics
print("\nCache statistics:")
print(client.get_cache_stats())
