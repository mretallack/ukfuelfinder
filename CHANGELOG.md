# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
