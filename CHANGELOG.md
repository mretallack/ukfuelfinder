# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-02

### Added
- Initial release
- OAuth 2.0 authentication with automatic token refresh
- Support for all Information Recipient API endpoints
- Fuel price retrieval (full and incremental)
- Forecourt information retrieval (full and incremental)
- Built-in caching with configurable TTL
- Rate limiting with automatic retry
- Comprehensive error handling
- Type hints throughout
- Full documentation and examples
- Python 3.8+ support

### Features
- Batch pagination (500 records per batch)
- Incremental updates via date_time parameter
- Environment variable configuration
- Cache statistics tracking
- Thread-safe operations

[1.0.0]: https://github.com/mretallack/ukfuelfinder/releases/tag/v1.0.0
