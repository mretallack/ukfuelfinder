# UK Fuel Finder Python Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Python library for accessing the UK Government Fuel Finder API.

## Features

- **OAuth 2.0 Authentication** - Automatic token management with refresh support
- **Comprehensive Data Access** - Fuel prices and forecourt information
- **Built-in Caching** - Reduces API calls with configurable TTL
- **Rate Limiting** - Automatic retry with exponential backoff
- **Type Hints** - Full type annotations for better IDE support
- **Extensive Error Handling** - Clear exceptions for all error cases
- **Batch Pagination** - Automatic handling of 500-record batches
- **Incremental Updates** - Fetch only changed data since a specific date

## Installation

```bash
pip install ukfuelfinder
```

## Quick Start

```python
from ukfuelfinder import FuelFinderClient

# Initialize client
client = FuelFinderClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    environment="production"  # or "test"
)

# Get all fuel prices
prices = client.get_all_pfs_prices()

# Search for stations near a location (returns list of (distance, PFSInfo) tuples)
nearby = client.search_by_location(latitude=51.5074, longitude=-0.1278, radius_km=5.0)
for distance, station in nearby:
    print(f"{distance:.2f}km - {station.trading_name}")

# Get prices for specific fuel type
unleaded_prices = client.get_prices_by_fuel_type("unleaded")

# Get forecourt information
forecourts = client.get_all_pfs_info()

# Get incremental updates since yesterday
from datetime import datetime, timedelta
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
updated_prices = client.get_incremental_price_updates(yesterday)
```

## Environment Variables

Set credentials via environment variables:

```bash
export FUEL_FINDER_CLIENT_ID="your_client_id"
export FUEL_FINDER_CLIENT_SECRET="your_client_secret"
export FUEL_FINDER_ENVIRONMENT="production"
```

Then initialize without parameters:

```python
client = FuelFinderClient()
```

## Documentation

- [Quick Start Guide](docs/quickstart.md)
- [API Reference](docs/api_reference.md)
- [Authentication](docs/authentication.md)
- [Caching Guide](docs/caching.md)
- [Rate Limiting](docs/rate_limiting.md)
- [Error Handling](docs/error_handling.md)

## Requirements

- Python 3.8+
- Valid Fuel Finder API credentials from [developer.fuel-finder.service.gov.uk](https://www.developer.fuel-finder.service.gov.uk)

## API Coverage

This library provides access to all Information Recipient API endpoints:

- **Authentication**
  - Generate OAuth access token
  - Refresh access token
  
- **Fuel Prices**
  - Fetch all PFS fuel prices (full or incremental)
  
- **Forecourt Information**
  - Fetch all PFS information (500 per batch)
  - Fetch incremental PFS information updates

## Examples

See the [examples/](examples/) directory for complete working examples:

- `basic_usage.py` - Simple getting started example
- `error_handling.py` - Comprehensive error handling
- `fetch_fuel_prices.py` - Fetch all fuel prices and save to JSON
- `fetch_all_sites.py` - Fetch all forecourt sites and save to JSON
- `location_search.py` - Search for stations near a location

## Development

### Setup

```bash
git clone https://github.com/mretallack/ukfuelfinder.git
cd ukfuelfinder
pip install -e .[dev]
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
black ukfuelfinder tests
mypy ukfuelfinder
flake8 ukfuelfinder
```

## Future Enhancements

Potential features for future development:

### Smart Fuel Recommendations
- **Cost-optimized routing** - Calculate total fuel cost including detour distance based on vehicle consumption
- **Cheapest fuel finder** - Find the most economical option considering current location, fuel prices, and distance
- **Route integration** - Suggest fuel stops along planned routes with minimal detour

### Price Intelligence
- **Price alerts** - Notify users when prices drop below a threshold in their area
- **Price forecasting** - Predict price trends based on historical data
- **Price comparison** - Compare prices across brands, regions, and fuel types

### Advanced Filtering
- **Multi-criteria search** - Filter by amenities (car wash, shop, 24-hour, EV charging)
- **Brand preferences** - Filter by preferred fuel brands or loyalty programs
- **Fuel type availability** - Find stations with specific fuel types (HVO, E10, premium diesel)

### Journey Planning
- **Fuel range calculator** - Estimate remaining range and suggest refuel points
- **Multi-stop optimization** - Plan optimal fuel stops for long journeys
- **Emergency fuel finder** - Quick search for nearest station when running low

### Data Analytics
- **Spending tracking** - Monitor fuel expenses over time
- **Savings calculator** - Calculate savings from using cheapest stations
- **Regional price analysis** - Compare average prices across different areas

### Integration Features
- **Navigation app integration** - Direct routing to selected stations
- **Calendar integration** - Schedule reminders for regular refueling
- **Vehicle integration** - Sync with vehicle telematics for automatic consumption data

Contributions implementing these features are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Data provided by the UK Government Fuel Finder service
- API documentation: [developer.fuel-finder.service.gov.uk](https://www.developer.fuel-finder.service.gov.uk)
- Content available under [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)

## Support

- **Issues**: [GitHub Issues](https://github.com/mretallack/ukfuelfinder/issues)
- **API Support**: [Contact Fuel Finder Team](https://www.developer.fuel-finder.service.gov.uk/contact-us)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
