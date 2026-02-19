#!/usr/bin/env python3
"""
Example: Migrating from Old API to New API (Feb 2025 Changes)

This example shows the differences between old and new API usage.
"""

from ukfuelfinder import FuelFinderClient

print("=" * 60)
print("OLD API (with backward compatibility)")
print("=" * 60)

# Old API usage - backward compatible mode (default)
client_old = FuelFinderClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    backward_compatible=True  # This is the default
)

pfs_list = client_old.get_all_pfs_prices(batch_number=1)
if pfs_list:
    pfs = pfs_list[0]
    print(f"\nStation: {pfs.trading_name}")
    print(f"Has 'success' field: {hasattr(pfs, 'success')}")  # True
    print(f"Has 'message' field: {hasattr(pfs, 'message')}")  # True
    if hasattr(pfs, 'success'):
        print(f"Success value: {pfs.success}")  # Always True
    if hasattr(pfs, 'message'):
        print(f"Message value: '{pfs.message}'")  # Always empty string

print("\n" + "=" * 60)
print("NEW API (without backward compatibility)")
print("=" * 60)

# New API usage - no backward compatibility
client_new = FuelFinderClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    backward_compatible=False
)

pfs_list = client_new.get_all_pfs_prices(batch_number=1)
if pfs_list:
    pfs = pfs_list[0]
    print(f"\nStation: {pfs.trading_name}")
    print(f"Has 'success' field: {hasattr(pfs, 'success')}")  # False
    print(f"Has 'message' field: {hasattr(pfs, 'message')}")  # False
    
    # New field available
    if pfs.fuel_prices:
        price = pfs.fuel_prices[0]
        print(f"\nFuel: {price.fuel_type}")
        print(f"Price: £{price.price/100:.2f}")
        if hasattr(price, 'price_change_effective_timestamp'):
            print(f"Effective timestamp: {price.price_change_effective_timestamp}")

print("\n" + "=" * 60)
print("MIGRATION RECOMMENDATION")
print("=" * 60)
print("""
For new code, use backward_compatible=False to avoid deprecated fields.
For existing code, keep backward_compatible=True until you can update
your code to not rely on 'success' and 'message' fields.

The deprecated fields will be removed in a future version.
""")
