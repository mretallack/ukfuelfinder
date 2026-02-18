# API Changes Implementation Tasks - February 17, 2025

## Overview
Implementation tasks for the February 17, 2025 API changes to the UK Fuel Finder API client library.

## Tasks

### 1. Update Response Models
- [x] Remove `success` and `message` fields from all response model classes
- [x] Add `price_change_effective_timestamp` field to appropriate response models
- [ ] Update model validation to exclude deprecated fields
- [ ] Update model tests to reflect new field structure

### 2. Create Backward Compatibility Layer
- [x] Create `BackwardCompatibleResponse` wrapper class
- [x] Implement adapter pattern for deprecated fields
- [x] Add configuration option for backward compatibility mode
- [x] Add deprecation warnings for compatibility mode

### 3. Update Error Handling
- [x] Create `BatchNotFoundError` exception class
- [x] Update HTTP client to handle 404 responses for invalid batch numbers
- [x] Add backward-compatible error handling for old clients
- [ ] Update error handling tests

### 4. Update Client Configuration
- [x] Add `backward_compatible` parameter to `FuelFinderClient` constructor
- [x] Add environment variable support (`UKFUELFINDER_BACKWARD_COMPATIBLE`)
- [ ] Implement global configuration option
- [ ] Add configuration tests

### 5. Update HTTP Client
- [x] Update response parsing to handle new field structure
- [x] Remove handling of `success` and `message` fields
- [x] Ensure double precision for latitude/longitude coordinates
- [ ] Update HTTP client tests

### 6. Create New Tests
- [x] Test backward compatibility mode
- [x] Test 404 error handling for invalid batch numbers
- [x] Test response parsing without deprecated fields
- [x] Test configuration options
- [x] Test adapter pattern functionality

### 7. Update Documentation
- [x] Update README with API changes section
- [x] Add migration guide for users
- [ ] Update code examples for new API
- [x] Update CHANGELOG with breaking changes
- [x] Document backward compatibility mode

### 8. Update Examples
- [x] Update example scripts to use new API
- [x] Add examples for backward compatibility mode
- [x] Add examples for error handling

### 9. Integration Testing
- [x] Test with real API (valid batch numbers)
- [ ] Test with real API (invalid batch numbers - expect 404)
- [x] Test backward compatibility with real API
- [x] Verify coordinate precision handling

### 10. Release Preparation
- [ ] Update version number in `pyproject.toml`
- [ ] Verify all tests pass
- [ ] Update package metadata
- [ ] Create release notes

## Dependencies
- Task 1 (Response Models) must be completed before Task 2 (Backward Compatibility)
- Task 3 (Error Handling) depends on Task 1
- Task 5 (HTTP Client) depends on Tasks 1 and 3
- Task 6 (Tests) depends on all implementation tasks
- Task 7 (Documentation) can be done in parallel with implementation

## Resources Needed
- API documentation for February 17, 2025 changes
- Test batch numbers (valid and invalid)
- Mock API responses without `success` and `message` fields
- Sample error responses (404 for invalid batch)

## Success Criteria
- All existing tests pass with backward compatibility enabled
- New tests for API changes pass
- Backward compatibility mode works as designed
- 404 errors are properly handled for invalid batch numbers
- Documentation is updated and accurate
- Code examples work with new API structure