"""Unit tests for models module."""
import pytest
from datetime import datetime
from ukfuelfinder.models import PFS, PFSInfo, FuelPrice, Address, Location


@pytest.mark.unit
class TestModels:
    """Tests for data models."""

    def test_fuel_price_from_dict(self):
        """Test FuelPrice creation from dictionary."""
        data = {
            "fuel_type": "unleaded",
            "price": 142.9,
            "currency": "GBP",
            "updated_at": "2026-02-02T18:00:00Z",
        }

        price = FuelPrice.from_dict(data)

        assert price.fuel_type == "unleaded"
        assert price.price == 142.9
        assert price.currency == "GBP"
        assert isinstance(price.updated_at, datetime)

    def test_pfs_from_dict(self, mock_pfs_response):
        """Test PFS creation from dictionary."""
        pfs = PFS.from_dict(mock_pfs_response[0])

        assert pfs.node_id == "0028acef5f3afc41c7e7d"
        assert pfs.mft_organisation_name == "789 LTD"
        assert pfs.trading_name == "FORECOURT 4"
        assert len(pfs.fuel_prices) == 2
        assert pfs.fuel_prices[0].fuel_type == "unleaded"

    def test_address_from_dict(self):
        """Test Address creation from dictionary."""
        data = {
            "line1": "123 High Street",
            "line2": None,
            "city": "London",
            "county": "Greater London",
            "postcode": "SW1A 1AA",
        }

        address = Address.from_dict(data)

        assert address.line1 == "123 High Street"
        assert address.city == "London"
        assert address.postcode == "SW1A 1AA"

    def test_location_from_dict(self):
        """Test Location creation from dictionary."""
        data = {"latitude": 51.5074, "longitude": -0.1278}

        location = Location.from_dict(data)

        assert location.latitude == 51.5074
        assert location.longitude == -0.1278

    def test_pfs_info_from_dict(self):
        """Test PFSInfo creation from dictionary."""
        data = {
            "node_id": "test123",
            "mft_organisation_name": "Test Org",
            "trading_name": "Test Station",
            "public_phone_number": "01234567890",
            "address": {
                "line1": "123 Street",
                "line2": None,
                "city": "London",
                "county": None,
                "postcode": "SW1A 1AA",
            },
            "location": {"latitude": 51.5, "longitude": -0.1},
            "brand": "TestBrand",
            "operator": "TestOp",
            "amenities": ["shop", "atm"],
        }

        pfs_info = PFSInfo.from_dict(data)

        assert pfs_info.node_id == "test123"
        assert pfs_info.address.postcode == "SW1A 1AA"
        assert pfs_info.location.latitude == 51.5
        assert "shop" in pfs_info.amenities
