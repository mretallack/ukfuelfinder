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

    line1: str
    line2: Optional[str]
    city: str
    county: Optional[str]
    postcode: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Address":
        """Create Address from API response dictionary."""
        return cls(
            line1=data["line1"],
            line2=data.get("line2"),
            city=data["city"],
            county=data.get("county"),
            postcode=data["postcode"],
        )


@dataclass
class Location:
    """Geographic coordinates."""

    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Location":
        """Create Location from API response dictionary."""
        return cls(latitude=float(data["latitude"]), longitude=float(data["longitude"]))


@dataclass
class PFSInfo:
    """Petrol Filling Station information (without prices)."""

    node_id: str
    mft_organisation_name: str
    trading_name: str
    public_phone_number: Optional[str]
    address: Optional[Address] = None
    location: Optional[Location] = None
    brand: Optional[str] = None
    operator: Optional[str] = None
    amenities: Optional[List[str]] = None
    opening_hours: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PFSInfo":
        """Create PFSInfo from API response dictionary."""
        address = Address.from_dict(data["address"]) if "address" in data else None
        location = Location.from_dict(data["location"]) if "location" in data else None

        return cls(
            node_id=data["node_id"],
            mft_organisation_name=data["mft_organisation_name"],
            trading_name=data["trading_name"],
            public_phone_number=data.get("public_phone_number"),
            address=address,
            location=location,
            brand=data.get("brand"),
            operator=data.get("operator"),
            amenities=data.get("amenities"),
            opening_hours=data.get("opening_hours"),
        )
