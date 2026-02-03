"""Unit tests for location search."""
import pytest
from ukfuelfinder.client import FuelFinderClient
from ukfuelfinder.models import PFSInfo, Location


@pytest.mark.unit
class TestLocationSearch:
    """Tests for location search functionality."""

    def test_haversine_distance(self):
        """Test haversine distance calculation."""
        # London to Paris (approx 344 km)
        london_lat, london_lon = 51.5074, -0.1278
        paris_lat, paris_lon = 48.8566, 2.3522
        
        distance = FuelFinderClient._haversine(london_lon, london_lat, paris_lon, paris_lat)
        
        assert 340 < distance < 350  # Approximate distance

    def test_search_by_location(self, monkeypatch):
        """Test search by location."""
        # Mock get_all_pfs_info
        mock_sites = [
            PFSInfo(
                node_id="site1",
                mft_organisation_name="Test Org 1",
                trading_name="Station 1",
                public_phone_number="123",
                location=Location(
                    latitude=51.5074,
                    longitude=-0.1278,
                    address_line_1="123 Street",
                    postcode="SW1A 1AA",
                ),
            ),
            PFSInfo(
                node_id="site2",
                mft_organisation_name="Test Org 2",
                trading_name="Station 2",
                public_phone_number="456",
                location=Location(
                    latitude=51.5174,
                    longitude=-0.1378,
                    address_line_1="456 Street",
                    postcode="SW1A 2BB",
                ),
            ),
            PFSInfo(
                node_id="site3",
                mft_organisation_name="Test Org 3",
                trading_name="Station 3",
                public_phone_number="789",
                location=Location(
                    latitude=52.0,
                    longitude=-1.0,
                    address_line_1="789 Street",
                    postcode="B1 1AA",
                ),
            ),
        ]
        
        client = FuelFinderClient(client_id="test", client_secret="test")
        monkeypatch.setattr(client, "get_all_pfs_info", lambda: mock_sites)
        
        # Search near London
        results = client.search_by_location(51.5074, -0.1278, radius_km=5.0)
        
        # Should find first two stations (within 5km), not the third
        assert len(results) == 2
        assert results[0][1].node_id == "site1"  # Closest
        assert results[1][1].node_id == "site2"
        
        # Results should be sorted by distance
        assert results[0][0] < results[1][0]

    def test_search_by_location_no_results(self, monkeypatch):
        """Test search with no results."""
        mock_sites = [
            PFSInfo(
                node_id="site1",
                mft_organisation_name="Test Org",
                trading_name="Station",
                public_phone_number="123",
                location=Location(
                    latitude=52.0,
                    longitude=-1.0,
                    address_line_1="123 Street",
                    postcode="B1 1AA",
                ),
            ),
        ]
        
        client = FuelFinderClient(client_id="test", client_secret="test")
        monkeypatch.setattr(client, "get_all_pfs_info", lambda: mock_sites)
        
        # Search far from the station
        results = client.search_by_location(51.5074, -0.1278, radius_km=1.0)
        
        assert len(results) == 0

    def test_search_by_location_missing_coordinates(self, monkeypatch):
        """Test search with sites missing coordinates."""
        mock_sites = [
            PFSInfo(
                node_id="site1",
                mft_organisation_name="Test Org",
                trading_name="Station",
                public_phone_number="123",
                location=None,  # No location
            ),
            PFSInfo(
                node_id="site2",
                mft_organisation_name="Test Org 2",
                trading_name="Station 2",
                public_phone_number="456",
                location=Location(
                    latitude=None,  # Missing latitude
                    longitude=-0.1278,
                    address_line_1="123 Street",
                    postcode="SW1A 1AA",
                ),
            ),
        ]
        
        client = FuelFinderClient(client_id="test", client_secret="test")
        monkeypatch.setattr(client, "get_all_pfs_info", lambda: mock_sites)
        
        # Should not crash, just return empty results
        results = client.search_by_location(51.5074, -0.1278, radius_km=5.0)
        
        assert len(results) == 0
