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

### 3. CSV Parser Updates

#### Current CSV Field Mapping
```python
CSV_FIELDS = {
    'latest_update_timestamp': 'latest_update',
    # ... other fields
}
```

#### Updated CSV Field Mapping
```python
CSV_FIELDS = {
    'forecourt_update_timestamp': 'forecourt_update',
    # ... other fields
}
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

### 4. CSV Processing
- **Field Mapping**: Update CSV field name mapping
- **Parser**: Update CSV parser to use new field name
- **Data Conversion**: Ensure timestamp format consistency

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
- Test CSV parsing with new field name
- Test coordinate precision handling

### 2. Integration Tests
- Test actual API calls with valid/invalid batch numbers
- Test CSV download and parsing
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
- CSV parser configuration
- Test data and mocks

### 2. External Dependencies
- API documentation updates
- CSV format specification
- Error code documentation

### 3. Testing Resources
- Test batch numbers (valid and invalid)
- Sample CSV files with new field name
- Mock API responses

## Migration Considerations

### 1. Breaking Changes
- Clients using `success` or `message` fields will break
- Clients expecting specific error codes for invalid batches will break
- CSV parsers using old field name will break

### 2. Versioning Strategy
- Consider API versioning if supporting old clients
- Document breaking changes clearly
- Provide migration guide for users

### 3. Rollout Plan
1. Update library code
2. Update tests
3. Release new version
4. Update documentation
5. Notify users of breaking changes