"""Test fixtures for UK Fuel Finder API."""

MOCK_TOKEN_RESPONSE = {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test_token",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "refresh_token_example",
}

MOCK_PFS_RESPONSE = [
    {
        "node_id": "0028acef5f3afc41c7e7d",
        "mft_organisation_name": "789 LTD",
        "public_phone_number": None,
        "trading_name": "FORECOURT 4",
        "fuel_prices": [
            {
                "fuel_type": "unleaded",
                "price": 142.9,
                "currency": "GBP",
                "updated_at": "2026-02-02T18:00:00Z",
            },
            {
                "fuel_type": "diesel",
                "price": 148.5,
                "currency": "GBP",
                "updated_at": "2026-02-02T18:00:00Z",
            },
        ],
    },
    {
        "node_id": "01da92125c37517670d4d",
        "mft_organisation_name": "VE3",
        "public_phone_number": "",
        "trading_name": "KHJH",
        "fuel_prices": [
            {
                "fuel_type": "unleaded",
                "price": 139.9,
                "currency": "GBP",
                "updated_at": "2026-02-02T17:30:00Z",
            }
        ],
    },
]

MOCK_PFS_INFO_RESPONSE = [
    {
        "node_id": "0028acef5f3afc41c7e7d",
        "mft_organisation_name": "Shell UK",
        "trading_name": "Shell Station",
        "public_phone_number": "01234567890",
        "address": {
            "line1": "123 High Street",
            "line2": None,
            "city": "London",
            "county": "Greater London",
            "postcode": "SW1A 1AA",
        },
        "location": {"latitude": 51.5074, "longitude": -0.1278},
        "brand": "Shell",
        "operator": "Shell UK",
        "amenities": ["shop", "atm", "car_wash"],
        "opening_hours": {"monday": "00:00-23:59"},
    }
]

MOCK_ERROR_RESPONSE = {"error": "unauthorized", "message": "Invalid or expired access token"}

# Fixtures for API responses without mft_organisation_name (Feb 25-26, 2026 changes)
MOCK_PFS_RESPONSE_NO_MFT = [
    {
        "node_id": "0028acef5f3afc41c7e7d",
        "public_phone_number": None,
        "trading_name": "FORECOURT 4",
        "fuel_prices": [
            {
                "fuel_type": "unleaded",
                "price": 142.9,
                "currency": "GBP",
                "updated_at": "2026-02-02T18:00:00Z",
            },
        ],
    },
]

MOCK_PFS_INFO_RESPONSE_NO_MFT = [
    {
        "node_id": "0028acef5f3afc41c7e7d",
        "trading_name": "Shell Station",
        "public_phone_number": "01234567890",
        "location": {"latitude": 51.5074, "longitude": -0.1278},
    }
]
