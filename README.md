# UK Fuel Finder Python Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Python library for accessing the UK Government Fuel Finder API.

## ⚠️ API Status Notice

**As of February 2, 2026** - The UK Fuel Finder API is experiencing significant performance issues on launch day:

- ✅ **Authentication endpoint** - Working
- ✅ **Fuel prices endpoint** (`/pfs/fuel-prices`) - Working (may be slow)
- ❌ **Forecourt info endpoint** (`/pfs`) - Returning 504 Gateway Timeout errors

The API infrastructure is struggling under load. This library is fully functional and tested - the issues are with the government API servers. See [this article](https://forecourttrader.co.uk/news/fuel-finder-25-of-forecourts-in-breach-of-law-as-system-goes-live/714726.article) for more details on the API problems.

**Recommendation**: Use `get_all_pfs_prices()` which works reliably. Avoid `get_all_pfs_info()` until the API stabilizes.

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
- `advanced_filtering.py` - Filtering and sorting prices
- `caching_example.py` - Cache configuration and usage
- `error_handling.py` - Comprehensive error handling

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
