"""
Data models for UK Fuel Finder API responses.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
from dateutil import parser


@dataclass
class FuelPrice:
    """Fuel price information."""

    fuel_type: str
    price: Optional[float]  # Can be null
    price_last_updated: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FuelPrice":
        """Create FuelPrice from API response dictionary."""
        price = None
        if data.get("price"):
            # Price comes as string like "0120.0000"
            price = float(data["price"])

        price_last_updated = None
        if data.get("price_last_updated"):
            price_last_updated = parser.parse(data["price_last_updated"])

        return cls(
            fuel_type=data["fuel_type"],
            price=price,
            price_last_updated=price_last_updated,
        )


@dataclass
class PFS:
    """Petrol Filling Station with fuel prices."""

    node_id: str
    mft_organisation_name: str
    trading_name: str
    public_phone_number: Optional[str]
    fuel_prices: List[FuelPrice]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PFS":
        """Create PFS from API response dictionary."""
        fuel_prices = [FuelPrice.from_dict(fp) for fp in data.get("fuel_prices", [])]
        return cls(
            node_id=data["node_id"],
            mft_organisation_name=data["mft_organisation_name"],
            trading_name=data["trading_name"],
            public_phone_number=data.get("public_phone_number"),
            fuel_prices=fuel_prices,
        )


@dataclass
class Address:
    """Station address information."""

    address_line_1: str
    address_line_2: Optional[str]
    city: str
    country: str
    county: Optional[str]
    postcode: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Address":
        """Create Address from API response dictionary."""
        return cls(
            address_line_1=data["address_line_1"],
            address_line_2=data.get("address_line_2"),
            city=data["city"],
            country=data["country"],
            county=data.get("county"),
            postcode=data["postcode"],
        )


@dataclass
class Location:
    """Geographic coordinates."""

    latitude: Optional[float]
    longitude: Optional[float]
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    county: Optional[str] = None
    postcode: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Location":
        """Create Location from API response dictionary."""
        latitude = float(data["latitude"]) if data.get("latitude") is not None else None
        longitude = float(data["longitude"]) if data.get("longitude") is not None else None
        
        return cls(
            latitude=latitude,
            longitude=longitude,
            address_line_1=data.get("address_line_1"),
            address_line_2=data.get("address_line_2"),
            city=data.get("city"),
            country=data.get("country"),
            county=data.get("county"),
            postcode=data.get("postcode"),
        )


@dataclass
class PFSInfo:
    """Petrol Filling Station information (without prices)."""

    node_id: str
    mft_organisation_name: str
    trading_name: str
    public_phone_number: Optional[str]
    is_same_trading_and_brand_name: Optional[bool] = None
    brand_name: Optional[str] = None
    temporary_closure: Optional[bool] = None
    permanent_closure: Optional[bool] = None
    permanent_closure_date: Optional[str] = None
    is_motorway_service_station: Optional[bool] = None
    is_supermarket_service_station: Optional[bool] = None
    location: Optional[Location] = None
    amenities: Optional[List[str]] = None
    opening_times: Optional[Dict[str, Any]] = None
    fuel_types: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PFSInfo":
        """Create PFSInfo from API response dictionary."""
        location = Location.from_dict(data["location"]) if "location" in data else None

        return cls(
            node_id=data["node_id"],
            mft_organisation_name=data["mft_organisation_name"],
            trading_name=data["trading_name"],
            public_phone_number=data.get("public_phone_number"),
            is_same_trading_and_brand_name=data.get("is_same_trading_and_brand_name"),
            brand_name=data.get("brand_name"),
            temporary_closure=data.get("temporary_closure"),
            permanent_closure=data.get("permanent_closure"),
            permanent_closure_date=data.get("permanent_closure_date"),
            is_motorway_service_station=data.get("is_motorway_service_station"),
            is_supermarket_service_station=data.get("is_supermarket_service_station"),
            location=location,
            amenities=data.get("amenities"),
            opening_times=data.get("opening_times"),
            fuel_types=data.get("fuel_types"),
        )
