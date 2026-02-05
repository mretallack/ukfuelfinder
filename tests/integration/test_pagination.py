"""Test for pagination bug - should fetch all stations, not just first batch."""
import pytest
from ukfuelfinder import FuelFinderClient
import os


@pytest.mark.integration
def test_get_all_stations_pagination():
    """Test that get_all_pfs_info fetches ALL stations, not just first batch."""
    client = FuelFinderClient(
        client_id=os.getenv("FUEL_FINDER_CLIENT_ID"),
        client_secret=os.getenv("FUEL_FINDER_CLIENT_SECRET"),
        timeout=60,
    )

    # Get all stations
    all_stations = client.get_all_pfs_info()

    # Should get more than 500 (first batch size)
    assert len(all_stations) > 500, f"Expected > 500 stations, got {len(all_stations)}"

    # Based on CSV, should be around 3,955 stations
    assert len(all_stations) > 3000, f"Expected > 3000 stations, got {len(all_stations)}"

    print(f"✅ Successfully fetched {len(all_stations)} stations")
