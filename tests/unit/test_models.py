"""Unit tests for models module."""

from datetime import datetime

import pytest

from ukfuelfinder.models import PFS, FuelPrice, Location, PFSInfo, Address


@pytest.mark.unit
class TestModels:
    """Tests for data models."""

    def test_fuel_price_from_dict(self):
        """Test FuelPrice creation from dictionary."""
        data = {
            "fuel_type": "E10",
            "price": "142.9000",
            "price_last_updated": "2026-02-02T18:00:00",
            "price_change_effective_timestamp": "2025-02-17T10:30:00Z",
        }

        price = FuelPrice.from_dict(data)

        assert price.fuel_type == "E10"
        assert price.price == 142.9
        assert isinstance(price.price_last_updated, datetime)
        assert isinstance(price.price_change_effective_timestamp, datetime)
        assert price.price_change_effective_timestamp.year == 2025

    def test_fuel_price_rejects_deprecated_fields(self):
        """Test FuelPrice rejects deprecated fields."""
        data = {
            "fuel_type": "E10",
            "price": "142.9000",
            "success": True,
        }

        with pytest.raises(ValueError, match="deprecated fields: success"):
            FuelPrice.from_dict(data)

    def test_pfs_from_dict(self, mock_pfs_response):
        """Test PFS creation from dictionary."""
        pfs = PFS.from_dict(mock_pfs_response[0])

        assert pfs.node_id == "0028acef5f3afc41c7e7d"
        assert pfs.mft_organisation_name == "789 LTD"
        assert pfs.trading_name == "FORECOURT 4"
        assert len(pfs.fuel_prices) == 2
        assert pfs.fuel_prices[0].fuel_type == "unleaded"

    def test_pfs_rejects_deprecated_fields(self):
        """Test PFS rejects deprecated fields."""
        data = {
            "node_id": "test123",
            "mft_organisation_name": "Test Org",
            "trading_name": "Test Station",
            "public_phone_number": None,
            "fuel_prices": [],
            "message": "Some message",
        }

        with pytest.raises(ValueError, match="deprecated fields: message"):
            PFS.from_dict(data)

    def test_location_from_dict(self):
        """Test Location creation from dictionary."""
        data = {
            "latitude": "51.5074",
            "longitude": "-0.1278",
            "address_line_1": "123 High Street",
            "city": "London",
            "postcode": "SW1A 1AA",
            "country": "England",
        }

        location = Location.from_dict(data)

        assert location.latitude == 51.5074
        assert location.longitude == -0.1278
        assert location.address_line_1 == "123 High Street"

    def test_location_rejects_deprecated_fields(self):
        """Test Location rejects deprecated fields."""
        data = {
            "latitude": "51.5074",
            "longitude": "-0.1278",
            "success": True,
            "message": "OK",
        }

        with pytest.raises(ValueError, match="deprecated fields"):
            Location.from_dict(data)

    def test_address_rejects_deprecated_fields(self):
        """Test Address rejects deprecated fields."""
        data = {
            "address_line_1": "123 Street",
            "address_line_2": None,
            "city": "London",
            "country": "England",
            "county": None,
            "postcode": "SW1A 1AA",
            "success": True,
        }

        with pytest.raises(ValueError, match="deprecated fields: success"):
            Address.from_dict(data)

    def test_pfs_info_from_dict(self):
        """Test PFSInfo creation from dictionary."""
        data = {
            "node_id": "test123",
            "mft_organisation_name": "Test Org",
            "trading_name": "Test Station",
            "public_phone_number": "01234567890",
            "brand_name": "TestBrand",
            "is_supermarket_service_station": True,
            "location": {
                "latitude": "51.5",
                "longitude": "-0.1",
                "address_line_1": "123 Street",
                "city": "London",
                "postcode": "SW1A 1AA",
                "country": "England",
            },
            "amenities": ["shop", "atm"],
            "fuel_types": ["E10", "B7_STANDARD"],
        }

        pfs_info = PFSInfo.from_dict(data)

        assert pfs_info.node_id == "test123"
        assert pfs_info.location.postcode == "SW1A 1AA"
        assert pfs_info.location.latitude == 51.5
        assert "shop" in pfs_info.amenities
        assert "E10" in pfs_info.fuel_types

    def test_pfs_info_rejects_deprecated_fields(self):
        """Test PFSInfo rejects deprecated fields."""
        data = {
            "node_id": "test123",
            "mft_organisation_name": "Test Org",
            "trading_name": "Test Station",
            "public_phone_number": None,
            "success": True,
        }

        with pytest.raises(ValueError, match="deprecated fields: success"):
            PFSInfo.from_dict(data)

    def test_pfs_without_mft_organisation_name(self):
        """Test PFS creation without mft_organisation_name field."""
        data = {
            "node_id": "test123",
            "trading_name": "Test Station",
            "public_phone_number": None,
            "fuel_prices": [],
        }

        pfs = PFS.from_dict(data)

        assert pfs.node_id == "test123"
        assert pfs.mft_organisation_name is None
        assert pfs.trading_name == "Test Station"

    def test_pfs_with_mft_organisation_name(self):
        """Test PFS creation with mft_organisation_name field."""
        data = {
            "node_id": "test123",
            "mft_organisation_name": "Test Org",
            "trading_name": "Test Station",
            "public_phone_number": None,
            "fuel_prices": [],
        }

        pfs = PFS.from_dict(data)

        assert pfs.node_id == "test123"
        assert pfs.mft_organisation_name == "Test Org"
        assert pfs.trading_name == "Test Station"

    def test_pfsinfo_without_mft_organisation_name(self):
        """Test PFSInfo creation without mft_organisation_name field."""
        data = {
            "node_id": "test123",
            "trading_name": "Test Station",
            "public_phone_number": "01234567890",
            "location": {"latitude": "51.5", "longitude": "-0.1"},
        }

        pfs_info = PFSInfo.from_dict(data)

        assert pfs_info.node_id == "test123"
        assert pfs_info.mft_organisation_name is None
        assert pfs_info.trading_name == "Test Station"

    def test_pfsinfo_with_mft_organisation_name(self):
        """Test PFSInfo creation with mft_organisation_name field."""
        data = {
            "node_id": "test123",
            "mft_organisation_name": "Test Org",
            "trading_name": "Test Station",
            "public_phone_number": "01234567890",
            "location": {"latitude": "51.5", "longitude": "-0.1"},
        }

        pfs_info = PFSInfo.from_dict(data)

        assert pfs_info.node_id == "test123"
        assert pfs_info.mft_organisation_name == "Test Org"
        assert pfs_info.trading_name == "Test Station"
