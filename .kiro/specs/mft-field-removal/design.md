# Design: MFT Organisation Name Field Removal

## Overview

Design for handling the removal of `mft_organisation_name` field from UK Fuel Finder API responses while maintaining backward compatibility.

## Architecture

### Component Changes

```
ukfuelfinder/
├── models.py              # Update PFS and PFSInfo dataclasses
tests/
├── unit/
│   └── test_models.py     # Add tests for optional field
└── fixtures/
    └── responses.py       # Add fixtures without mft_organisation_name
docs/
├── openapi.json           # Replace with info-recipent.en.json
└── README.md              # Document the change
README.md                  # Update main documentation
CHANGELOG.md               # Add version entry
```

## Data Model Changes

### Current State

```python
@dataclass
class PFS:
    node_id: str
    mft_organisation_name: str  # Required field
    trading_name: str
    public_phone_number: Optional[str]
    fuel_prices: List[FuelPrice]
```

### New State

```python
@dataclass
class PFS:
    node_id: str
    mft_organisation_name: Optional[str]  # Now optional
    trading_name: str
    public_phone_number: Optional[str]
    fuel_prices: List[FuelPrice]
```

### Implementation

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> "PFS":
    """Create PFS from API response dictionary."""
    _validate_no_deprecated_fields(data)
    
    fuel_prices = [FuelPrice.from_dict(fp) for fp in data.get("fuel_prices", [])]
    return cls(
        node_id=data["node_id"],
        mft_organisation_name=data.get("mft_organisation_name"),  # Use .get() instead of direct access
        trading_name=data["trading_name"],
        public_phone_number=data.get("public_phone_number"),
        fuel_prices=fuel_prices,
    )
```

## Sequence Diagram

```
User Code -> FuelFinderClient: get_all_pfs_prices()
FuelFinderClient -> API: GET /v1/pfs/fuel-prices
API -> FuelFinderClient: Response (no mft_organisation_name)
FuelFinderClient -> PFS.from_dict(): Parse response
PFS.from_dict() -> PFS: Create with mft_organisation_name=None
PFS -> User Code: Return PFS object
User Code -> PFS: Access mft_organisation_name
PFS -> User Code: Return None (no error)
```

## Test Strategy

### Unit Tests

**Test Case 1: PFS without mft_organisation_name**
```python
def test_pfs_without_mft_organisation_name():
    data = {
        "node_id": "123",
        "trading_name": "Test Station",
        "fuel_prices": []
    }
    pfs = PFS.from_dict(data)
    assert pfs.mft_organisation_name is None
```

**Test Case 2: PFS with mft_organisation_name**
```python
def test_pfs_with_mft_organisation_name():
    data = {
        "node_id": "123",
        "mft_organisation_name": "Test Org",
        "trading_name": "Test Station",
        "fuel_prices": []
    }
    pfs = PFS.from_dict(data)
    assert pfs.mft_organisation_name == "Test Org"
```

**Test Case 3: PFSInfo without mft_organisation_name**
```python
def test_pfsinfo_without_mft_organisation_name():
    data = {
        "node_id": "123",
        "trading_name": "Test Station",
        "location": {"latitude": 51.5, "longitude": -0.1}
    }
    info = PFSInfo.from_dict(data)
    assert info.mft_organisation_name is None
```

**Test Case 4: PFSInfo with mft_organisation_name**
```python
def test_pfsinfo_with_mft_organisation_name():
    data = {
        "node_id": "123",
        "mft_organisation_name": "Test Org",
        "trading_name": "Test Station",
        "location": {"latitude": 51.5, "longitude": -0.1}
    }
    info = PFSInfo.from_dict(data)
    assert info.mft_organisation_name == "Test Org"
```

### Integration Tests

Update existing integration tests to handle None values gracefully.

## Documentation Updates

### README.md

Add to API Changes section:
```markdown
### February 25-26, 2026 Changes

- **Removed Field**: `mft_organisation_name` removed from all API responses
- **Impact**: Field is now `Optional[str]` and will be `None` in new responses
- **Migration**: Check for `None` before using: `if pfs.mft_organisation_name:`
```

### CHANGELOG.md

```markdown
## [2.0.1] - 2026-02-XX

### Changed
- **Breaking API Change**: `mft_organisation_name` field removed from UK Fuel Finder API
- Made `mft_organisation_name` optional in PFS and PFSInfo models
- Field now returns `None` instead of string value

### Fixed
- Backward compatibility maintained - existing code continues to work
- Models handle API responses without `mft_organisation_name` field

### Updated
- OpenAPI specification to match current API (February 25-26, 2026)
- Documentation to reflect field removal
- Tests to cover both presence and absence of field
```

### docs/openapi.json

Replace entire file with content from `docs/info-recipent.en.json`.

## Implementation Considerations

### Type Checking

- Update type hints: `str` → `Optional[str]`
- Mypy will catch any code assuming non-None value
- Users will get type hints showing field is optional

### Error Handling

No new error handling needed:
- Field access returns None (not an error)
- Existing None checks will work
- New code should check for None before use

### Performance

- No performance impact
- `.get()` method has same performance as direct access
- Optional type has no runtime overhead

### Backward Compatibility

**Maintains compatibility:**
- Existing code accessing field gets None instead of error
- Code checking `if pfs.mft_organisation_name:` works correctly
- No changes required to existing user code

**Breaking scenarios (acceptable):**
- Code assuming field is always a string will get None
- Code doing string operations without None check may fail
- This is expected behavior for API breaking change

## Migration Guide

### For Library Users

**Before (old API):**
```python
pfs = client.get_all_pfs_prices()[0]
print(pfs.mft_organisation_name)  # Always a string
```

**After (new API):**
```python
pfs = client.get_all_pfs_prices()[0]
if pfs.mft_organisation_name:
    print(pfs.mft_organisation_name)  # May be None
else:
    print("Organisation name not available")
```

## Rollout Plan

1. Update models.py with Optional type
2. Update test fixtures with both scenarios
3. Add new unit tests
4. Update integration tests
5. Replace docs/openapi.json
6. Update README.md and CHANGELOG.md
7. Run full test suite
8. Commit and create release

## Validation

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Type checking passes (mypy)
- [ ] Linting passes (flake8)
- [ ] Code coverage ≥ 80%
- [ ] Documentation updated
- [ ] OpenAPI spec updated

## Alternatives Considered

### Alternative 1: Remove field entirely
**Rejected:** Would break all existing code accessing the field

### Alternative 2: Default to empty string
**Rejected:** None is more semantically correct for missing data

### Alternative 3: Add deprecation warning
**Rejected:** Field is already removed from API, warning not helpful

## Selected Approach

Make field `Optional[str]` with default None:
- ✅ Backward compatible
- ✅ Type-safe
- ✅ Semantically correct
- ✅ Minimal code changes
- ✅ No new dependencies
