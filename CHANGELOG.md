# Changelog

All notable changes to this project will be documented in this file.

## [3.0.0] - 2026-02-26

### Changed
- **Breaking API Change**: `mft_organisation_name` field removed from UK Fuel Finder API (February 25-26, 2026)
- Made `mft_organisation_name` optional (`Optional[str]`) in `PFS` and `PFSInfo` models
- Field now returns `None` instead of string value in new API responses

### Fixed
- Backward compatibility maintained - existing code continues to work without modification
- Models handle API responses without `mft_organisation_name` field gracefully
- No exceptions raised when field is missing from API response

### Updated
- OpenAPI specification updated to match current API (February 25-26, 2026)
- Documentation updated to reflect field removal and optional nature
- Added tests for both presence and absence of `mft_organisation_name` field
- README.md includes migration guidance for handling optional field

### Technical Details
- All 70 unit tests passing
- 85% code coverage maintained
- Type hints updated: `str` → `Optional[str]`
- No breaking changes to public API

## [2.0.0] - 2025-02-19

### Added
- **Global Configuration**: `set_global_backward_compatible()` function for application-wide settings
- **HTTP Client Tests**: Comprehensive test suite for HTTP client (10 new tests)
- **Global Config Tests**: Test suite for global configuration (6 new tests)
- **Integration Test**: Test for invalid batch number 404 handling
- **New Examples**: 
  - `examples/api_migration.py` - Migration guide from old to new API
  - `examples/global_config.py` - Global configuration usage
- **Enhanced Documentation**: Updated all examples for new API format

### Changed
- **Version Bump**: Major version to 2.0.0 for API changes
- **HTTP Client**: Enhanced response parsing for both old and new API formats
- **Configuration Priority**: Global config > Environment variable > Constructor parameter > Default
- **Test Coverage**: Increased to 74% (58 tests passing)
- **Examples**: Updated `basic_usage.py` to demonstrate new API

### Fixed
- **HTTP Client**: Proper handling of response formats with and without data wrapper
- **Error Handling**: Improved 404 detection for batch endpoints
- **Mock Tests**: Fixed elapsed time mocking in HTTP client tests

### Documentation
- Updated README with comprehensive API changes section
- Added detailed migration guide
- Updated all code examples for new API
- Created release notes (RELEASE_NOTES_2.0.0.md)

### Technical Details
- All 58 unit tests passing
- 74% code coverage
- HTTP client now at 96% coverage
- Backward compatibility fully tested

## [1.3.0] - 2025-02-17

### Added
- **Backward Compatibility Mode**: Added backward compatibility for API changes
- **New Exception Types**: Added `BatchNotFoundError` and `InvalidBatchNumberError` for better error handling
- **BackwardCompatibleResponse**: Wrapper class for backward compatibility with deprecated fields
- **Environment Variable Support**: `UKFUELFINDER_BACKWARD_COMPATIBLE` environment variable
- **New Configuration**: `backward_compatible` parameter in `FuelFinderClient` constructor

### Changed
- **API Changes Support**: Updated to handle February 17, 2025 API changes
- **Error Handling**: Updated to handle new 404 responses for invalid batch numbers
- **Response Models**: Added `price_change_effective_timestamp` field to FuelPrice model
- **HTTP Client**: Updated to handle new API response formats

### Fixed
- **Error Handling**: Proper handling of 404 errors for invalid batch numbers
- **Response Parsing**: Fixed handling of API responses without `success` and `message` fields
- **Backward Compatibility**: Old code using `success` and `message` fields continues to work

### Breaking Changes
- **API Changes**: The UK Fuel Finder API has been updated with breaking changes:
  - Removed `success` and `message` fields from all responses
  - Added `price_change_effective_timestamp` field to fuel price responses
  - Invalid batch numbers now return HTTP 404 (was 400)
  - Latitude/longitude coordinates now use double precision

### Migration
- Set `backward_compatible=True` (default) to maintain compatibility
- Update code to not rely on `success` and `message` fields
- Handle new `price_change_effective_timestamp` field in fuel price data
- Update error handling for 404 responses on invalid batch numbers

## [1.2.0] - 2026-02-17

### Fixed
- Handle null latitude/longitude coordinates gracefully in Location model
- Fixed black formatting issues in price_service.py and models.py
- Added default batch_number=1 for incremental updates

### Added
- OpenAPI specification documentation in docs/openapi.json
- Release procedure documentation in README.md

### Changed
- Location.latitude and Location.longitude now Optional[float] to handle null values
- Improved error handling for API responses with missing coordinate data
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-05

### Fixed
- Pagination bug where `get_all_pfs_info()` and `get_all_pfs_prices()` only returned first 500 records
- Now automatically fetches all batches when `batch_number=None` (default behavior)
- Fetches complete dataset of 6,800+ stations instead of just first batch

### Added
- `get_all_pfs_prices_paginated()` method for automatic pagination
- Location search functionality with `search_by_location(latitude, longitude, radius_km)`
- Haversine distance calculation for geographic searches
- Integration test for pagination verification

### Changed
- `get_all_pfs_info()` and `get_all_pfs_prices()` now fetch all data by default
- Maintains backwards compatibility with explicit `batch_number` parameter
- Improved documentation with location search examples

## [1.0.0] - 2026-02-02

### Added
- Initial release
- OAuth 2.0 authentication with automatic token refresh (JSON request format)
- Support for UK Fuel Finder Information Recipient API endpoints
- Fuel price retrieval (full and incremental)
- Forecourt information retrieval (full and incremental)
- Built-in caching with configurable TTL (15min prices, 1hr forecourts)
- Rate limiting with automatic retry (30 RPM test, 120 RPM production)
- Comprehensive error handling (11 exception types)
- Type hints throughout
- Full documentation and examples
- Python 3.8+ support

### Features
- Batch pagination (500 records per batch using batch-number parameter)
- Incremental updates via effective-start-timestamp parameter
- Environment variable configuration (.env support)
- Cache statistics tracking
- Thread-safe operations

### API Details
- Authentication: POST /v1/oauth/generate_access_token (JSON body)
- Fuel Prices: GET /v1/pfs/fuel-prices
- Forecourt Info: GET /v1/pfs
- Response format: Nested JSON with {"success": true, "data": [...]}
- Fuel types: E10, E5, B7_STANDARD, B7_PREMIUM, B10, HVO
- Models: PFS, PFSInfo, FuelPrice, Location (with embedded address)

[1.0.0]: https://github.com/mretallack/ukfuelfinder/releases/tag/v1.0.0
