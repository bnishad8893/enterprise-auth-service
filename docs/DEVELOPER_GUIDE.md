# Developer Guide

Coding standards, contribution guidelines, and development practices.

## Code Style

### Python

Follow PEP 8 with these specific rules:

- Line length: Maximum 88 characters (enforced by Black)
- Indentation: 4 spaces
- Use type hints for all function signatures
- Use docstrings for all public functions, classes, and modules

### Formatting

- Use Black for code formatting (auto-format on save in VS Code)
- Use isort for import organization
- Use Ruff for linting

Run formatting before committing:

```bash
black src/ tests/
isort src/ tests/
ruff check --fix src/ tests/
```

## Type Hints

All functions must have type hints:

```python
from typing import Optional, List

def get_user_by_email(email: str) -> Optional[User]:
    """Retrieve user by email address.

    Args:
        email: User email address

    Returns:
        User object or None if not found
    """
    return User.objects.filter(email=email).first()
```

## Docstrings

Use Google-style docstrings:

```python
def process_payment(amount: float, user_id: str) -> bool:
    """Process payment for user.

    Args:
        amount: Payment amount in cents
        user_id: Unique user identifier

    Returns:
        True if payment processed successfully

    Raises:
        PaymentException: If payment fails
        ValidationError: If amount is invalid
    """
```

## Testing Requirements

### Coverage

- Minimum 80% code coverage for all modules
- 100% coverage for authentication and security modules
- Run coverage before committing: `pytest --cov=src`

### Test Structure

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_serializers.py
│   └── test_services.py
├── integration/
│   ├── test_api.py
│   └── test_database.py
└── fixtures/
    └── factories.py
```

### Naming Conventions

Test names follow: `test_<function>_<scenario>_<expected_outcome>`

```python
def test_authenticate_with_valid_credentials_returns_token():
    """Test successful authentication returns JWT token."""

def test_authenticate_with_invalid_password_raises_error():
    """Test authentication fails with invalid password."""
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_models.py

# Run specific test
pytest tests/unit/test_models.py::test_user_model_creation

# Run with coverage
pytest --cov=src --cov-report=html
```

## Git Workflow

### Branch Naming

- Feature: `feature/auth-jwt-implementation`
- Fix: `fix/password-reset-token-expiration`
- Documentation: `docs/api-reference`
- Release: `release/1.0.0`

### Commits

- Write clear, descriptive commit messages
- Use present tense: "Add feature" not "Added feature"
- Reference issues when applicable: "Fixes #123"
- Keep commits focused on single concerns

Example:
```
Add JWT authentication endpoints

- Implement token generation and validation
- Add refresh token mechanism
- Add tests for authentication flow

Fixes #45
```

### Pull Requests

1. Keep PRs focused and reasonably sized
2. Link related issues in PR description
3. Ensure CI/CD checks pass
4. Request review from team members
5. Address review comments or discuss
6. Rebase on main before merging

## Architecture Principles

### Clean Architecture

- Separate business logic from framework code
- Domain entities are independent
- Use interfaces for external dependencies
- Dependency injection for testability

### SOLID Principles

- **S**ingle Responsibility: Classes have one reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subclasses can replace parent classes
- **I**nterface Segregation: Specific interfaces over general ones
- **D**ependency Inversion: Depend on abstractions, not implementations

## Code Organization

### Project Structure

```
src/
├── api/           # REST endpoints
├── core/          # Business logic
├── models/        # Database models
├── serializers/   # Serialization/validation
├── services/      # Business operations
├── utils/         # Utilities and helpers
├── middleware/    # Custom middleware
├── auth/          # Authentication logic
└── config/        # Configuration
```

### Module Organization

Each module should be self-contained:

```python
# Single file module
module/
├── __init__.py
├── serializers.py
├── services.py
├── views.py
└── urls.py
```

## Security Guidelines

- Never commit secrets or credentials
- Use environment variables for configuration
- Sanitize all user input
- Use parameterized queries
- Validate data on both client and server
- Use HTTPS in production
- Keep dependencies updated

## Performance Considerations

- Use Django ORM `select_related()` and `prefetch_related()` appropriately
- Index database columns used in queries
- Cache frequently accessed data in Redis
- Use Celery for long-running tasks
- Profile before optimizing
- Use pagination for large result sets

## Documentation

- Update README when adding features
- Document architectural decisions in `docs/ARCHITECTURE_DECISIONS.md`
- Keep API documentation synchronized with code
- Add inline comments for non-obvious logic
- Document environment variables and configuration

## CI/CD Integration

All pull requests must:

- Pass automated tests
- Achieve minimum coverage (80%)
- Pass linting checks (Ruff, MyPy, Black)
- Have code review approval
- Have passing GitHub Actions workflows

## Debugging

### Debug Print

Avoid leaving debug prints in code. Use logging instead:

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Processing user: %s", user_id)
logger.info("User created: %s", user.email)
logger.warning("Deprecated endpoint used: %s", endpoint)
logger.error("Failed to process payment: %s", str(error))
```

### Django Shell

```bash
python manage.py shell

# Query in shell
from src.models import User
User.objects.filter(email='user@example.com')
```

## Dependency Management

- Keep dependencies minimal
- Regularly update dependencies
- Check security advisories
- Document reasons for major dependencies
- Use requirements-*.txt files for different environments

## Performance Profiling

```bash
# Profile Django request
python -m cProfile -s cumtime manage.py runserver
```

## Review Checklist

Before submitting PR:

- [ ] Code follows style guidelines
- [ ] Tests written and passing
- [ ] Coverage maintained
- [ ] Documentation updated
- [ ] No security issues
- [ ] No hardcoded values/secrets
- [ ] Commits are clean and descriptive
- [ ] Rebased on latest main

