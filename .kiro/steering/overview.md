# UK Fuel Finder Python Library - Project Overview

## Project Summary

Python library for accessing the UK Government Fuel Finder API. Provides OAuth 2.0 authentication, comprehensive data access to fuel prices and forecourt information, with built-in caching and rate limiting.

**Current Version:** 2.0.0  
**License:** MIT  
**Python Support:** 3.8+

## Key Features

- OAuth 2.0 authentication with automatic token management
- Fuel prices and forecourt information access
- Built-in caching with configurable TTL
- Rate limiting with exponential backoff
- Full type hints
- Batch pagination (500-record batches)
- Incremental updates support
- Backward compatibility mode for API changes

## Project Structure

```
ukfuelfinder/
├── __init__.py           # Package exports and version
├── client.py             # Main FuelFinderClient class
├── auth.py               # OAuth authentication
├── http_client.py        # HTTP request handling
├── models.py             # Data models (PFS, FuelPrice, etc.)
├── config.py             # Configuration management
├── cache.py              # Caching implementation
├── rate_limiter.py       # Rate limiting
├── exceptions.py         # Custom exceptions
├── compatibility.py      # Backward compatibility layer
└── services/
    ├── price_service.py      # Fuel price operations
    └── forecourt_service.py  # Forecourt info operations

tests/
├── unit/                 # Unit tests
├── integration/          # Integration tests
└── fixtures/             # Test fixtures

examples/                 # Usage examples
docs/                     # Documentation
```

## API Status

⚠️ **Current Issue:** UK Government API experiencing severe performance issues (as of Feb 4, 2026)
- Authentication works
- Data endpoints timing out
- Library is functional, waiting for government API fix

## Recent Changes (v2.0.0)

### API Breaking Changes (Feb 17, 2025)
- Removed: `success` and `message` fields from responses
- Added: `price_change_effective_timestamp` field
- Changed: Invalid batch numbers return HTTP 404
- Changed: Lat/long use double precision

### Backward Compatibility
- Enabled by default via `backward_compatible=True`
- Environment variable: `UKFUELFINDER_BACKWARD_COMPATIBLE`
- Allows gradual migration from old API format

## Development Workflow

### Setup
```bash
git clone https://github.com/mretallack/ukfuelfinder.git
cd ukfuelfinder
pip install -e .[dev]
```

### Testing
```bash
pytest                    # Run all tests
pytest tests/unit/        # Unit tests only
pytest tests/integration/ # Integration tests only
```

### Code Quality
```bash
black ukfuelfinder tests  # Format code
mypy ukfuelfinder         # Type checking
flake8 ukfuelfinder       # Linting
```

## Release Procedure

### 1. Update Version
Update version in all three files:
- `pyproject.toml` → `version = "X.Y.Z"`
- `setup.py` → `version="X.Y.Z"`
- `ukfuelfinder/__init__.py` → `__version__ = "X.Y.Z"`

### 2. Update Changelog
Add new version entry to `CHANGELOG.md` with:
- Version number and date
- Added features
- Changed functionality
- Fixed bugs
- Breaking changes (if any)

### 3. Commit and Push
```bash
git add pyproject.toml setup.py ukfuelfinder/__init__.py CHANGELOG.md
git commit -m "Release: vX.Y.Z"
git push origin main
```

### 4. Create GitHub Release
1. Go to GitHub repository → Releases → Create new release
2. Tag: `vX.Y.Z` (must match version in files)
3. Title: `vX.Y.Z`
4. Description: Copy from CHANGELOG.md for this version
5. Publish release

### 5. Automated Publishing
- GitHub Actions automatically builds and publishes to PyPI
- Workflow: `.github/workflows/publish.yml`
- Triggered by creating a new release tag

## Configuration

### Environment Variables
```bash
export FUEL_FINDER_CLIENT_ID="your_client_id"
export FUEL_FINDER_CLIENT_SECRET="your_client_secret"
export FUEL_FINDER_ENVIRONMENT="production"  # or "test"
export UKFUELFINDER_BACKWARD_COMPATIBLE=1    # Enable backward compatibility
```

### Client Initialization
```python
from ukfuelfinder import FuelFinderClient

# With credentials
client = FuelFinderClient(
    client_id="your_id",
    client_secret="your_secret",
    environment="production",
    backward_compatible=True
)

# From environment variables
client = FuelFinderClient()
```

## Core API Methods

### Fuel Prices
- `get_all_pfs_prices()` - Fetch all fuel prices
- `get_prices_by_fuel_type(fuel_type)` - Filter by fuel type
- `get_incremental_price_updates(since_date)` - Get updates since date

### Forecourt Information
- `get_all_pfs_info()` - Fetch all forecourt information
- `get_incremental_pfs_updates(since_date)` - Get updates since date

### Location Search
- `search_by_location(lat, lon, radius_km)` - Find stations near location

## Testing Strategy

### Unit Tests
- Mock external dependencies
- Test individual components
- Fast execution
- Located in `tests/unit/`

### Integration Tests
- Test against real API (when available)
- Require valid credentials
- Slower execution
- Located in `tests/integration/`

### Coverage Target
- Minimum 80% code coverage
- Enforced by pytest configuration

## Dependencies

### Core
- `requests>=2.31.0` - HTTP client
- `python-dateutil>=2.8.0` - Date handling

### Development
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `responses>=0.23.0` - HTTP mocking
- `black>=23.0.0` - Code formatting
- `mypy>=1.0.0` - Type checking
- `flake8>=6.0.0` - Linting

## Future Enhancements

Potential features documented in README.md:
- Smart fuel recommendations with cost-optimized routing
- Price intelligence and forecasting
- Advanced filtering by amenities
- Journey planning integration
- Data analytics and spending tracking

## Resources

- **Repository:** https://github.com/mretallack/ukfuelfinder
- **PyPI:** https://pypi.org/project/ukfuelfinder/
- **API Docs:** https://developer.fuel-finder.service.gov.uk
- **Issues:** https://github.com/mretallack/ukfuelfinder/issues
- **License:** MIT (see LICENSE file)

## Support

- GitHub Issues for bug reports and feature requests
- API support via Fuel Finder Team contact form
- Data available under Open Government Licence v3.0
