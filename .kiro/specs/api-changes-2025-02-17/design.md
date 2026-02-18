# API Changes Design - February 17, 2025

## Technical Architecture

### 1. Response Model Updates

#### Current Response Structure
```python
class FuelPriceResponse:
    success: bool
    message: str
    latitude: float
    longitude: float
    # ... other fields
```

#### Updated Response Structure
```python
class FuelPriceResponse:
    latitude: float  # Now double precision
    longitude: float  # Now double precision
    price_change_effective_timestamp: str
    # ... other fields (success and message removed)
```

### 2. Error Handling Updates

#### Current Error Handling
```python
# Invalid batch number might return 400 or other error
if response.status_code == 400:
    raise InvalidBatchNumberError()
```

#### Updated Error Handling
```python
# Invalid batch number now returns 404
if response.status_code == 404:
    raise BatchNotFoundError()
```



## Component Interactions

### Sequence Diagram: Fetch API Call

```
Client -> API: GET /fuel-prices/{batch}
API -> Database: Validate batch number
Database -> API: Batch not found
API -> Client: HTTP 404 Not Found
```

### Sequence Diagram: Successful Response

```
Client -> API: GET /fuel-prices/{valid-batch}
API -> Database: Retrieve fuel prices
Database -> API: Return data with double precision coordinates
API -> Client: Response without success/message fields
```

## Implementation Considerations

### 1. Data Type Changes
- **Latitude/Longitude**: Change from `float` to `double` in Python (both are `float` type)
- **Impact**: No code changes needed for type declaration, but ensure precision handling

### 2. Response Schema Changes
- **Removal**: Remove `success` and `message` fields from all response models
- **Addition**: Add `price_change_effective_timestamp` field
- **Validation**: Update response validation logic

### 3. Error Handling
- **New Exception**: Create `BatchNotFoundError` exception class
- **Status Codes**: Update error handling to check for 404
- **Backward Compatibility**: Consider if old clients need special handling



## Error Handling Approaches

### 1. Batch Number Validation
```python
def fetch_fuel_prices(batch_number: str) -> FuelPriceResponse:
    response = api_client.get(f"/fuel-prices/{batch_number}")
    
    if response.status_code == 404:
        raise BatchNotFoundError(f"Batch {batch_number} not found")
    
    # ... rest of processing
```

### 2. Response Validation
```python
def validate_response(data: dict) -> FuelPriceResponse:
    # Ensure success and message fields are not present
    if 'success' in data or 'message' in data:
        raise InvalidResponseError("Response contains deprecated fields")
    
    # Ensure new field is present
    if 'price_change_effective_timestamp' not in data:
        raise InvalidResponseError("Missing price_change_effective_timestamp")
    
    return FuelPriceResponse(**data)
```

## Testing Strategy

### 1. Unit Tests
- Test 404 responses for invalid batch numbers
- Test response parsing without success/message fields
- Test coordinate precision handling

### 2. Integration Tests
- Test actual API calls with valid/invalid batch numbers
- Test error handling scenarios

### 3. Mock Data
```python
# Mock response without success/message fields
mock_response = {
    "latitude": 51.5074,
    "longitude": -0.1278,
    "price_change_effective_timestamp": "2025-02-17T10:30:00Z",
    # ... other fields
}
```

## Dependencies and Resources

### 1. Required Changes
- Response model classes
- Error handling logic
- Test data and mocks

### 2. External Dependencies
- API documentation updates
- Error code documentation

### 3. Testing Resources
- Test batch numbers (valid and invalid)
- Mock API responses

## Backward Compatibility Strategy

### 1. Compatibility Goals
- **Primary Goal**: Maintain API call compatibility for existing users
- **Secondary Goal**: Gracefully handle breaking changes from upstream API
- **Approach**: Use adapter patterns and configuration options

### 2. Adapter Pattern Implementation

#### Response Adapter for Deprecated Fields
```python
class BackwardCompatibleResponse:
    def __init__(self, new_response: FuelPriceResponse):
        self._response = new_response
        
    @property
    def success(self) -> bool:
        """Always return True for backward compatibility"""
        return True
        
    @property 
    def message(self) -> str:
        """Return empty string for backward compatibility"""
        return ""
        
    def __getattr__(self, name):
        """Delegate all other attributes to the new response"""
        return getattr(self._response, name)
```

#### Configuration Option
```python
class FuelFinderClient:
    def __init__(self, backward_compatible: bool = False):
        self.backward_compatible = backward_compatible
        
    def get_fuel_prices(self, batch_number: str) -> Union[FuelPriceResponse, BackwardCompatibleResponse]:
        response = self._fetch_from_api(batch_number)
        
        if self.backward_compatible:
            return BackwardCompatibleResponse(response)
        return response
```

### 3. Error Handling Compatibility

#### Unified Error Handling
```python
def handle_batch_error(status_code: int, batch_number: str):
    if status_code == 404:
        if config.BACKWARD_COMPATIBLE:
            # Return old-style error for compatibility
            raise InvalidBatchNumberError(f"Invalid batch number: {batch_number}")
        else:
            # Return new-style error
            raise BatchNotFoundError(f"Batch {batch_number} not found")
    # ... other error handling
```



### 5. Versioning and Configuration

#### Library Configuration
```python
import ukfuelfinder.config as config

# Option 1: Global configuration
config.BACKWARD_COMPATIBLE = True

# Option 2: Per-client configuration
client = FuelFinderClient(backward_compatible=True)

# Option 3: Environment variable
# UKFUELFINDER_BACKWARD_COMPATIBLE=1
```

#### Version Detection
```python
def detect_api_version() -> str:
    """Detect which API version is being used"""
    try:
        response = test_api_call()
        if 'success' in response:
            return 'legacy'
        elif 'price_change_effective_timestamp' in response:
            return '2025-02-17'
        else:
            return 'unknown'
    except Exception:
        return 'unknown'
```

### 6. Migration Path

#### Phase 1: Dual Support (v1.3.0)
- Add backward compatibility mode (default: enabled)
- Support both old and new field names
- Log deprecation warnings

#### Phase 2: Transition (v1.4.0)
- Change default to disabled
- Stronger deprecation warnings
- Provide migration tools

#### Phase 3: Cleanup (v2.0.0)
- Remove backward compatibility code
- Require new API version
- Clear breaking change

### 7. User Communication

#### Deprecation Warnings
```python
import warnings

if config.BACKWARD_COMPATIBLE:
    warnings.warn(
        "Backward compatibility mode is enabled. This will be removed in v2.0.0. "
        "Update your code to use the new API format.",
        DeprecationWarning,
        stacklevel=2
    )
```

#### Documentation
- Clear migration guide in README
- Code examples for both old and new APIs
- Version compatibility matrix

### 8. Documentation Updates

#### README Updates Required
1. **API Changes Section**: Document February 17, 2025 breaking changes
2. **Backward Compatibility**: Explain compatibility mode and configuration
3. **Migration Guide**: Step-by-step instructions for updating code
4. **Code Examples**: Updated examples showing new API usage
5. **Configuration**: Document `backward_compatible` parameter and environment variable

#### CHANGELOG Updates Required
1. **Version Entry**: Add entry for v1.3.0 with API changes
2. **Breaking Changes**: List all breaking changes from upstream API
3. **New Features**: Document backward compatibility mode
4. **Deprecations**: Note deprecated fields and behaviors
5. **Migration Path**: Guide for users updating from previous versions

#### Example README Update
```markdown
## API Changes (February 17, 2025)

The UK Fuel Finder API has been updated with breaking changes:

### Breaking Changes
1. **Removed Fields**: `success` and `message` fields removed from responses
2. **New Field**: `price_change_effective_timestamp` added to responses
3. **Error Codes**: Invalid batch numbers now return HTTP 404 (Not Found)


### Backward Compatibility
This library includes backward compatibility mode (enabled by default):

```python
# Old code continues to work
client = FuelFinderClient(backward_compatible=True)
prices = client.get_fuel_prices("batch123")
print(prices.success)  # Returns True
print(prices.message)  # Returns empty string

# New code without compatibility
client = FuelFinderClient(backward_compatible=False)
prices = client.get_fuel_prices("batch123")
# prices.success and prices.message not available
```

### Migration
1. Update to v1.3.0 or later
2. Test with `backward_compatible=True`
3. Update code to remove `success` and `message` field usage
4. Handle 404 errors for invalid batch numbers
5. Switch to `backward_compatible=False`
```

### 9. Test Updates Required

#### New Unit Tests
1. **Backward Compatibility Tests**
```python
def test_backward_compatibility_mode():
    client = FuelFinderClient(backward_compatible=True)
    response = client.get_fuel_prices("test-batch")
    assert hasattr(response, 'success')
    assert hasattr(response, 'message')
    assert response.success is True
    assert response.message == ""

def test_forward_compatibility_mode():
    client = FuelFinderClient(backward_compatible=False)
    response = client.get_fuel_prices("test-batch")
    assert not hasattr(response, 'success')
    assert not hasattr(response, 'message')
    assert hasattr(response, 'price_change_effective_timestamp')
```

2. **Error Handling Tests**
```python
def test_404_error_handling():
    client = FuelFinderClient()
    with pytest.raises(BatchNotFoundError):
        client.get_fuel_prices("invalid-batch")

def test_backward_compatible_error_handling():
    client = FuelFinderClient(backward_compatible=True)
    with pytest.raises(InvalidBatchNumberError):
        client.get_fuel_prices("invalid-batch")
```



4. **Configuration Tests**
```python
def test_environment_variable_config():
    os.environ['UKFUELFINDER_BACKWARD_COMPATIBLE'] = '1'
    client = FuelFinderClient()
    assert client.backward_compatible is True
    
def test_deprecation_warnings():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        client = FuelFinderClient(backward_compatible=True)
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
```

5. **Response Model Tests**
```python
def test_response_model_without_deprecated_fields():
    data = {
        'latitude': 51.5074,
        'longitude': -0.1278,
        'price_change_effective_timestamp': '2025-02-17T10:30:00Z'
    }
    response = FuelPriceResponse(**data)
    assert response.latitude == 51.5074
    assert response.longitude == -0.1278
    assert response.price_change_effective_timestamp == '2025-02-17T10:30:00Z'
    
def test_backward_compatible_response_wrapper():
    original = FuelPriceResponse(
        latitude=51.5074,
        longitude=-0.1278,
        price_change_effective_timestamp='2025-02-17T10:30:00Z'
    )
    wrapped = BackwardCompatibleResponse(original)
    assert wrapped.success is True
    assert wrapped.message == ""
    assert wrapped.latitude == 51.5074
    assert wrapped.price_change_effective_timestamp == '2025-02-17T10:30:00Z'
```

#### Integration Tests
1. **API Version Detection Test**
```python
def test_api_version_detection():
    version = detect_api_version()
    assert version in ['legacy', '2025-02-17', 'unknown']
```

2. **End-to-End Compatibility Test**
```python
def test_end_to_end_backward_compatibility():
    # Test full flow with backward compatibility
    client = FuelFinderClient(backward_compatible=True)
    
    # Should work with old field access patterns
    prices = client.get_fuel_prices("valid-batch")
    assert prices.success is not None
    assert prices.message is not None
    
    # Should also work with new fields
    assert hasattr(prices, 'price_change_effective_timestamp')
```

#### Test Data Updates
1. **Mock Response Data**: Update test fixtures to remove `success` and `message` fields
2. **Error Response Mocks**: Add 404 response mocks for invalid batch tests

4. **Configuration Test Data**: Add test data for different compatibility modes

## Migration Considerations

### 1. Breaking Changes
- Clients using `success` or `message` fields will break without compatibility mode
- Clients expecting specific error codes for invalid batches will break


### 2. Versioning Strategy
- Use semantic versioning: breaking changes in major versions
- Provide backward compatibility in minor versions
- Document breaking changes clearly
- Provide migration guide for users

### 3. Rollout Plan
1. Update library code with backward compatibility
2. Update tests for both old and new behavior
3. Release new version with compatibility enabled by default
4. Update documentation with migration guide
5. Notify users of upcoming changes
6. In future version, disable compatibility by default
7. In major version, remove compatibility code