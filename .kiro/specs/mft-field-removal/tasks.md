# Tasks: MFT Organisation Name Field Removal

## Implementation Tasks

### Phase 1: Model Updates

- [ ] **Task 1.1: Update PFS model**
  - Update `mft_organisation_name` type from `str` to `Optional[str]`
  - Update `from_dict()` to use `.get()` instead of direct access
  - File: `ukfuelfinder/models.py`
  - Expected: PFS model accepts missing field

- [ ] **Task 1.2: Update PFSInfo model**
  - Update `mft_organisation_name` type from `str` to `Optional[str]`
  - Update `from_dict()` to use `.get()` instead of direct access
  - File: `ukfuelfinder/models.py`
  - Expected: PFSInfo model accepts missing field

### Phase 2: Test Updates

- [ ] **Task 2.1: Add test fixtures**
  - Add fixture for PFS without `mft_organisation_name`
  - Add fixture for PFSInfo without `mft_organisation_name`
  - File: `tests/fixtures/responses.py`
  - Expected: Fixtures available for testing

- [ ] **Task 2.2: Add unit tests for PFS**
  - Test PFS creation without `mft_organisation_name`
  - Test PFS creation with `mft_organisation_name`
  - File: `tests/unit/test_models.py`
  - Expected: Both scenarios pass

- [ ] **Task 2.3: Add unit tests for PFSInfo**
  - Test PFSInfo creation without `mft_organisation_name`
  - Test PFSInfo creation with `mft_organisation_name`
  - File: `tests/unit/test_models.py`
  - Expected: Both scenarios pass

- [ ] **Task 2.4: Run test suite**
  - Execute: `pytest tests/ -v`
  - Expected: All tests pass, coverage ≥ 80%

### Phase 3: Documentation Updates

- [ ] **Task 3.1: Update OpenAPI specification**
  - Replace `docs/openapi.json` with content from `docs/info-recipent.en.json`
  - File: `docs/openapi.json`
  - Expected: OpenAPI spec reflects current API

- [ ] **Task 3.2: Update README.md**
  - Add section for February 25-26, 2026 API changes
  - Document `mft_organisation_name` field removal
  - Add migration guidance
  - File: `README.md`
  - Expected: Users understand the change

- [ ] **Task 3.3: Update CHANGELOG.md**
  - Add version 2.0.1 entry
  - Document breaking change
  - Document backward compatibility
  - File: `CHANGELOG.md`
  - Expected: Change history updated

### Phase 4: Quality Assurance

- [ ] **Task 4.1: Run type checking**
  - Execute: `mypy ukfuelfinder`
  - Expected: No type errors

- [ ] **Task 4.2: Run linting**
  - Execute: `flake8 ukfuelfinder`
  - Expected: No linting errors

- [ ] **Task 4.3: Run code formatting**
  - Execute: `black ukfuelfinder tests`
  - Expected: Code formatted

- [ ] **Task 4.4: Verify test coverage**
  - Execute: `pytest --cov=ukfuelfinder --cov-report=term-missing`
  - Expected: Coverage ≥ 80%

### Phase 5: Version and Release

- [ ] **Task 5.1: Update version numbers**
  - Update `pyproject.toml` to version 2.0.1
  - Update `setup.py` to version 2.0.1
  - Update `ukfuelfinder/__init__.py` to version 2.0.1
  - Expected: Version consistent across files

- [ ] **Task 5.2: Final test run**
  - Execute: `pytest tests/ -v`
  - Expected: All tests pass

- [ ] **Task 5.3: Commit changes**
  - Commit all changes with message: "Fix: Make mft_organisation_name optional for API compatibility"
  - Expected: Changes committed to feature branch

- [ ] **Task 5.4: Push feature branch**
  - Push to origin: `git push origin feature/mft-field-removal`
  - Expected: Branch available on GitHub

- [ ] **Task 5.5: Merge to main**
  - Merge feature branch to main
  - Expected: Changes in main branch

- [ ] **Task 5.6: Create release**
  - Tag version: `git tag v2.0.1`
  - Push tag: `git push origin v2.0.1`
  - Create GitHub release from tag
  - Expected: Release published, PyPI updated

## Dependencies

- docs/info-recipent.en.json must exist
- All tests must pass before merging
- Code quality checks must pass

## Success Criteria

- ✅ All unit tests pass
- ✅ All integration tests pass
- ✅ Type checking passes
- ✅ Linting passes
- ✅ Code coverage ≥ 80%
- ✅ Documentation updated
- ✅ Version bumped to 2.0.1
- ✅ Changes merged to main
- ✅ Release published
