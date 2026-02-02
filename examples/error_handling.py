"""
Error handling example for UK Fuel Finder API
"""
from ukfuelfinder import FuelFinderClient
from ukfuelfinder.exceptions import (
    AuthenticationError,
    RateLimitError,
    TimeoutError,
    ServerError,
)

client = FuelFinderClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Handle authentication errors
try:
    prices = client.get_all_pfs_prices()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    print("Check your credentials")

# Handle rate limiting
try:
    for i in range(200):
        prices = client.get_all_pfs_prices(batch_number=i)
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    print(f"Retry after: {e.retry_after} seconds")

# Handle timeouts
try:
    client_with_short_timeout = FuelFinderClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        timeout=1  # 1 second
    )
    prices = client_with_short_timeout.get_all_pfs_prices()
except TimeoutError as e:
    print(f"Request timed out: {e}")

# Handle server errors
try:
    prices = client.get_all_pfs_prices()
except ServerError as e:
    print(f"Server error: {e}")
