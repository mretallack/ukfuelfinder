# Requirements: MFT Organisation Name Field Removal

## Overview

Handle the removal of `mft_organisation_name` field from UK Fuel Finder API (effective February 25-26, 2026) while maintaining backward compatibility with existing code.

## User Stories

### US-1: Backward Compatible Field Handling
**As a** library user with existing code  
**I want** my code to continue working without changes  
**So that** I don't have to update my application immediately

**Acceptance Criteria:**
- WHEN the API returns data without `mft_organisation_name`
- THE SYSTEM SHALL set the field to None
- AND existing code accessing the field SHALL NOT raise exceptions

### US-2: Optional Field Access
**As a** library user  
**I want** to access `mft_organisation_name` when available  
**So that** I can handle both old and new API responses

**Acceptance Criteria:**
- WHEN `mft_organisation_name` is present in API response
- THE SYSTEM SHALL populate the field with the value
- WHEN `mft_organisation_name` is absent in API response
- THE SYSTEM SHALL set the field to None

### US-3: Model Validation
**As a** library maintainer  
**I want** models to validate correctly with optional fields  
**So that** data integrity is maintained

**Acceptance Criteria:**
- WHEN creating PFS from dict without `mft_organisation_name`
- THE SYSTEM SHALL create valid PFS object with field set to None
- WHEN creating PFSInfo from dict without `mft_organisation_name`
- THE SYSTEM SHALL create valid PFSInfo object with field set to None

### US-4: Test Coverage
**As a** library maintainer  
**I want** comprehensive tests for optional field handling  
**So that** the change is verified to work correctly

**Acceptance Criteria:**
- WHEN tests run with data missing `mft_organisation_name`
- THE SYSTEM SHALL pass all tests
- WHEN tests run with data containing `mft_organisation_name`
- THE SYSTEM SHALL pass all tests

### US-5: Documentation Updates
**As a** library user  
**I want** updated documentation reflecting the field removal  
**So that** I understand the API changes

**Acceptance Criteria:**
- WHEN reading README.md
- THE SYSTEM SHALL document the field removal and optional nature
- WHEN reading CHANGELOG.md
- THE SYSTEM SHALL list the breaking change and mitigation
- WHEN reading docs/openapi.json
- THE SYSTEM SHALL reflect the updated API specification

### US-6: OpenAPI Specification Sync
**As a** library maintainer  
**I want** the OpenAPI spec updated from the official source  
**So that** documentation matches the actual API

**Acceptance Criteria:**
- WHEN docs/openapi.json is updated
- THE SYSTEM SHALL use the content from docs/info-recipent.en.json
- AND the specification SHALL reflect current API structure

## Technical Requirements

### TR-1: Type Safety
- `mft_organisation_name` must be typed as `Optional[str]`
- Type hints must be updated in both PFS and PFSInfo models

### TR-2: Backward Compatibility
- Existing code must continue to work without modification
- No breaking changes to public API
- Field access returns None instead of raising AttributeError

### TR-3: Test Updates
- Unit tests must cover both presence and absence of field
- Integration tests must handle new API responses
- Mock data must include both scenarios

### TR-4: Documentation
- README.md must document the change
- CHANGELOG.md must include version entry
- docs/openapi.json must be updated from official source
- Code examples must show optional field handling

## Non-Functional Requirements

### NFR-1: Performance
- No performance degradation from optional field handling

### NFR-2: Compatibility
- Python 3.8+ support maintained
- No new dependencies required

### NFR-3: Code Quality
- Maintain 80%+ test coverage
- Pass all linting and type checking
- Follow existing code style

## Out of Scope

- Changes to other fields not mentioned in release notes
- Migration tools for existing databases
- Automatic data backfill for missing fields

## Dependencies

- docs/info-recipent.en.json (official API spec)
- UK Fuel Finder API February 25-26, 2026 changes

## Risks

- **Risk:** Existing code may assume field is always present
  - **Mitigation:** Make field optional, return None instead of error
  
- **Risk:** Tests may fail with None values
  - **Mitigation:** Update tests to handle both scenarios

## Success Metrics

- All existing tests pass
- New tests cover optional field scenarios
- Documentation updated and accurate
- No breaking changes to public API
