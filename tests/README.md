# Tests

This directory contains all automated tests.

## Structure

- **unit/**: Unit tests for individual components
- **integration/**: Integration tests for modules working together
- **e2e/**: End-to-end tests for complete workflows
- **fixtures/**: Shared test data and fixtures
- **conftest.py**: Pytest configuration and shared utilities

## Testing Standards

- Minimum 80% code coverage
- All critical paths covered by tests
- Tests are independent and can run in any order
- Test naming follows `test_<function>_<scenario>_<expected_outcome>`
- Use factories for consistent test data generation

## Running Tests

Check documentation for test execution commands and CI/CD integration.
