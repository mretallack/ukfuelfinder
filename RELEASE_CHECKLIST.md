# Release Checklist - Version 2.0.0

## Pre-Release Verification

### Code Quality
- [x] All 58 unit tests passing
- [x] Test coverage at 74% (exceeds 65% requirement)
- [x] No failing tests
- [x] Code formatted with black
- [x] Type hints verified

### Version Updates
- [x] `pyproject.toml` version updated to 2.0.0
- [x] `ukfuelfinder/__init__.py` version updated to 2.0.0
- [x] CHANGELOG.md updated with 2.0.0 entry
- [x] Release notes created (RELEASE_NOTES_2.0.0.md)

### Documentation
- [x] README.md updated with API changes
- [x] Migration guide included
- [x] All code examples updated
- [x] New examples created:
  - examples/api_migration.py
  - examples/global_config.py
- [x] CHANGELOG.md comprehensive

### Testing
- [x] Unit tests: 58 passing
- [x] HTTP client tests: 10 tests
- [x] Global config tests: 6 tests
- [x] Integration test for 404 handling added
- [x] Backward compatibility tested
- [x] Error handling tested

### Features Implemented
- [x] Global configuration support
- [x] Environment variable support
- [x] Backward compatibility mode
- [x] BatchNotFoundError exception
- [x] Enhanced HTTP client
- [x] Priority-based configuration

## Release Steps

### 1. Final Verification
```bash
# Run all tests
python3 -m pytest tests/unit/ -v

# Check coverage
python3 -m pytest tests/unit/ --cov=ukfuelfinder --cov-report=term-missing

# Verify version
python3 -c "import ukfuelfinder; print(ukfuelfinder.__version__)"
```

### 2. Git Operations
```bash
# Stage all changes
git add -A

# Commit
git commit -m "Release: Version 2.0.0 - API Changes Feb 2025

- Implement global configuration for backward compatibility
- Add comprehensive HTTP client tests
- Update all examples for new API format
- Add integration test for invalid batch 404 handling
- Update version to 2.0.0
- Create release notes and update CHANGELOG

All 58 tests passing with 74% coverage."

# Tag release
git tag -a v2.0.0 -m "Version 2.0.0 - API Changes February 2025"

# Push
git push origin main
git push origin v2.0.0
```

### 3. Build Package
```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build
python3 -m build

# Verify build
ls -lh dist/
```

### 4. Test Package
```bash
# Install in test environment
pip install dist/ukfuelfinder-2.0.0-py3-none-any.whl

# Test import
python3 -c "import ukfuelfinder; print(ukfuelfinder.__version__)"

# Run quick test
python3 -c "from ukfuelfinder import set_global_backward_compatible; print('OK')"
```

### 5. Publish to PyPI
```bash
# Upload to Test PyPI first
python3 -m twine upload --repository testpypi dist/*

# Test install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ ukfuelfinder

# Upload to PyPI
python3 -m twine upload dist/*
```

### 6. GitHub Release
- Go to https://github.com/mretallack/ukfuelfinder/releases
- Click "Draft a new release"
- Tag: v2.0.0
- Title: "Version 2.0.0 - API Changes February 2025"
- Description: Copy from RELEASE_NOTES_2.0.0.md
- Attach dist files
- Publish release

### 7. Post-Release
- [ ] Verify PyPI page updated
- [ ] Test installation: `pip install ukfuelfinder`
- [ ] Verify documentation renders correctly
- [ ] Update any external documentation
- [ ] Announce release (if applicable)

## Rollback Plan

If issues are discovered:

1. Remove PyPI release (if possible)
2. Revert git tag: `git tag -d v2.0.0 && git push origin :refs/tags/v2.0.0`
3. Revert commit: `git revert HEAD`
4. Fix issues
5. Re-release as 2.0.1

## Success Criteria

- [x] All tests pass
- [x] Version numbers consistent
- [x] Documentation complete
- [x] Backward compatibility maintained
- [x] New features working
- [ ] Package published to PyPI
- [ ] GitHub release created
- [ ] Installation verified

## Notes

- This is a major version bump (2.0.0) due to API changes
- Backward compatibility is maintained by default
- Deprecation timeline: 6 months (until August 2025)
- Next breaking change: Version 3.0.0 (remove backward compatibility)
