# Release Notes - Version 2.0.0

**Release Date:** February 19, 2025

## Overview

This major release implements the UK Government Fuel Finder API changes effective February 17, 2025. The API has removed deprecated `success` and `message` fields from all responses. This library provides full backward compatibility while supporting the new API format.

## Breaking Changes

### API Response Format Changes

The UK Government API no longer returns `success` and `message` fields in responses:

**Old Format (deprecated):**
```json
{
  "success": true,
  "message": "",
  "data": [...]
}
```

**New Format:**
```json
{
  "data": [...]
}
```

### Library Changes

- Response objects no longer have `success` and `message` attributes by default
- New `BatchNotFoundError` exception for invalid batch numbers (404 responses)
- HTTP client now properly handles 404 errors on batch endpoints

## New Features

### 1. Backward Compatibility Mode

Enable backward compatibility to maintain existing code:

```python
from ukfuelfinder import FuelFinderClient

# Backward compatible (default)
client = FuelFinderClient(
    client_id="your_id",
    client_secret="your_secret",
    backward_compatible=True  # Default
)

# Access deprecated fields
pfs = client.get_all_pfs_prices()[0]
print(pfs.success)  # Always True
print(pfs.message)  # Always empty string
```

### 2. Global Configuration

Set backward compatibility globally for all client instances:

```python
import ukfuelfinder

# Set globally
ukfuelfinder.set_global_backward_compatible(False)

# All clients will use new API format
client = ukfuelfinder.FuelFinderClient(...)
```

### 3. Environment Variable Support

Control backward compatibility via environment variable:

```bash
export UKFUELFINDER_BACKWARD_COMPATIBLE=false
```

Priority order:
1. Global configuration (highest)
2. Environment variable
3. Constructor parameter
4. Default value (True)

### 4. New Exception: BatchNotFoundError

Specific exception for invalid batch numbers:

```python
from ukfuelfinder import FuelFinderClient
from ukfuelfinder.exceptions import BatchNotFoundError

client = FuelFinderClient(...)

try:
    prices = client.get_all_pfs_prices(batch_number=99999)
except BatchNotFoundError as e:
    print(f"Invalid batch: {e}")
```

### 5. Enhanced HTTP Client

- Handles both old and new API response formats
- Proper 404 error handling for batch endpoints
- Improved response parsing with data wrapper support

## Migration Guide

### For New Projects

Use the new API format without backward compatibility:

```python
client = FuelFinderClient(
    client_id="your_id",
    client_secret="your_secret",
    backward_compatible=False
)
```

### For Existing Projects

#### Option 1: Keep Backward Compatibility (Recommended Initially)

No changes needed. The library defaults to backward compatible mode:

```python
# This continues to work
client = FuelFinderClient(...)
pfs = client.get_all_pfs_prices()[0]
print(pfs.success)  # Still works
```

#### Option 2: Migrate to New API

1. Remove code that accesses `success` and `message` fields
2. Set `backward_compatible=False`
3. Test thoroughly

```python
# Before
if pfs.success:
    print(pfs.trading_name)

# After (just remove the check)
print(pfs.trading_name)
```

## Testing

All tests pass with 74% code coverage:
- 58 unit tests
- 10 new HTTP client tests
- 6 global configuration tests
- Integration tests for 404 handling

## Documentation Updates

- Updated README with API changes section
- Added migration guide
- Updated all code examples
- New examples:
  - `examples/api_migration.py` - Migration guide
  - `examples/global_config.py` - Global configuration usage

## Deprecation Notice

The backward compatibility mode will be maintained for at least 6 months. The `success` and `message` fields will be removed in version 3.0.0 (estimated August 2025).

## Technical Details

### New Files
- `tests/unit/test_http_client.py` - HTTP client tests
- `tests/unit/test_global_config.py` - Global configuration tests
- `examples/api_migration.py` - Migration example
- `examples/global_config.py` - Global config example

### Modified Files
- `ukfuelfinder/config.py` - Added global configuration
- `ukfuelfinder/client.py` - Priority-based backward compatibility
- `ukfuelfinder/http_client.py` - Enhanced response handling
- `ukfuelfinder/__init__.py` - Export global config function
- `examples/basic_usage.py` - Updated for new API

## Upgrade Instructions

```bash
pip install --upgrade ukfuelfinder
```

## Compatibility

- Python 3.8+
- Supports both old and new API formats
- No breaking changes if using default settings

## Contributors

- Mark Retallack (@mretallack)

## Links

- [GitHub Repository](https://github.com/mretallack/ukfuelfinder)
- [API Documentation](https://www.fuel-finder.service.gov.uk/api/v1/docs)
- [Issue Tracker](https://github.com/mretallack/ukfuelfinder/issues)
