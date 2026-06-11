"""Test for stations that exist but have no price data."""

import os

import pytest

from ukfuelfinder import FuelFinderClient


@pytest.mark.integration
def test_murco_wool_station_has_prices():
    """Test that Murco-Wool station in Wool, Dorset has price data.

    This test documents a known issue where some stations exist in the
    station database but have no prices reported to the API.

    Station: Wool and Bovington Motors (Murco-Wool)
    Location: Wool, Dorset (50.6833, -2.2167)
    Node ID: c068821c665146c482d8ea34f3879efbab64ac2a7865a8f9a80014c29450ce91
    """
    client = FuelFinderClient(
        client_id=os.getenv("FUEL_FINDER_CLIENT_ID"),
        client_secret=os.getenv("FUEL_FINDER_CLIENT_SECRET"),
        timeout=60,
    )

    # Search near Wool, Dorset
    lat, lon = 50.6833, -2.2167
    radius = 10.0

    nearby_stations = client.search_by_location(lat, lon, radius)

    # Find Murco-Wool station
    murco_station = None
    for distance, station in nearby_stations:
        if "murco" in station.brand_name.lower() and "wool" in station.brand_name.lower():
            murco_station = station
            break

    assert murco_station is not None, "Murco-Wool station not found in location search"

    print(f"\n✅ Found station: {murco_station.trading_name}")
    print(f"   Brand: {murco_station.brand_name}")
    print(f"   Node ID: {murco_station.node_id}")
    print(f"   Fuel types available: {murco_station.fuel_types}")

    # Get all price data
    all_pfs = client.get_all_pfs_prices()

    # Check if station has prices
    station_prices = None
    for pfs in all_pfs:
        if pfs.node_id == murco_station.node_id:
            station_prices = pfs
            break

    # This assertion will FAIL if the station has no prices
    assert station_prices is not None, (
        f"Station {murco_station.trading_name} exists but has no price data in API. "
        f"Node ID: {murco_station.node_id}"
    )

    # If we get here, check that it has actual prices
    prices_with_values = [fp for fp in station_prices.fuel_prices if fp.price is not None]

    assert (
        len(prices_with_values) > 0
    ), f"Station {murco_station.trading_name} has price records but all prices are None"

    print(f"\n✅ Station has {len(prices_with_values)} prices:")
    for fp in prices_with_values:
        print(f"   {fp.fuel_type}: {fp.price}p")
