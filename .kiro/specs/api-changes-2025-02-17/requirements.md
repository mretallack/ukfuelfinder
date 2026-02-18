# API Changes Requirements - February 17, 2025

## Overview
API changes announced on February 17, 2025 that require updates to the UK Fuel Finder API client library.

## Changes Summary

### 1. Data Type Changes
- **Change**: Latitude and longitude values are now represented using the `double` data type
- **Impact**: Improved precision and consistency across services

### 2. Error Handling
- **Change**: Invalid batch numbers now return HTTP 404 (Not Found) instead of previous behavior
- **Impact**: Need to handle 404 errors for invalid batch numbers

### 3. Response Schema Changes
- **Removed Fields**: `success` and `message` fields removed from Fetch API responses
- **New Field**: `price_change_effective_timestamp` field added to provide visibility into pricing updates
- **Note**: Future pricing information is not included in responses

### 4. CSV Format Changes
- **Change**: `latest_update_timestamp` field renamed to `forecourt_update_timestamp`
- **Impact**: CSV parsing logic needs to be updated

## EARS Notation Requirements

### 1. Data Type Precision
**WHEN** the API returns latitude/longitude coordinates  
**THE SYSTEM SHALL** use double precision floating point numbers  
**TO ENSURE** consistent coordinate precision across all services

### 2. Error Handling
**WHEN** a request contains an invalid batch number  
**THE SYSTEM SHALL** return HTTP 404 (Not Found)  
**TO ENSURE** consistent error handling for invalid batch numbers

### 3. Response Schema
**WHEN** the Fetch API returns a response  
**THE SYSTEM SHALL** exclude the `success` and `message` fields  
**AND SHALL** include the new `price_change_effective_timestamp` field  
**TO ENSURE** alignment with updated API specification

### 4. CSV Field Names
**WHEN** processing CSV data  
**THE SYSTEM SHALL** use `forecourt_update_timestamp` field name  
**INSTEAD OF** the previous `latest_update_timestamp`  
**TO ENSURE** compatibility with updated CSV format

### 5. Future Pricing
**WHEN** retrieving pricing information  
**THE SYSTEM SHALL NOT** include future pricing data  
**TO ENSURE** only current pricing information is provided

## Impact Assessment
- **Breaking Changes**: Yes - response schema changes
- **Data Type Changes**: Latitude/longitude precision increased
- **Error Handling**: New 404 responses for invalid batch numbers
- **CSV Format**: Field name changes require CSV parser updates
- **Backward Compatibility**: Not backward compatible with previous API versions

## Implementation Priority
1. Update response models to remove `success` and `message` fields
2. Update CSV parsing to use `forecourt_update_timestamp`
3. Update error handling for 404 responses
4. Update coordinate handling to use double precision
5. Add `price_change_effective_timestamp` field support