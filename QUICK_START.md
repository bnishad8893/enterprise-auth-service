# Quick Reference Guide

Essential commands and resources for developing in this repository.

## 📖 Documentation Quick Links

### Getting Started
- [Setup Guide](docs/SETUP_GUIDE.md) - Local development setup
- [Developer Guide](docs/DEVELOPER_GUIDE.md) - Coding standards
- [Project Structure](STRUCTURE.md) - Directory organization

### Architecture & Design
- [System Design](architecture/SYSTEM_DESIGN.md) - System architecture
- [Database Design](architecture/DATABASE_DESIGN.md) - Database schema
- [Security Architecture](architecture/SECURITY_ARCHITECTURE.md) - Security model
- [Architecture Decisions](docs/ARCHITECTURE_DECISIONS.md) - ADRs

### Operations
- [API Documentation](docs/API_DOCUMENTATION.md) - REST API reference
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Production deployment
- [Foundation Summary](FOUNDATION.md) - Complete overview

---

## 🚀 Development Commands (Coming Soon)

```bash
# Environment setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Running development server
python manage.py runserver

# Database operations
python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser

# Testing
pytest                    # Run all tests
pytest --cov            # With coverage report
pytest tests/unit/      # Specific directory

# Code quality
black src/ tests/       # Format code
ruff check --fix src/   # Lint and fix
mypy src/              # Type checking
```

---

## 🐳 Docker Commands (Coming Soon)

```bash
# Development with Docker Compose
docker-compose up -d        # Start services
docker-compose down         # Stop services
docker-compose logs -f      # View logs

# Database in Docker
docker-compose exec db psql -U postgres -d dev_db

# Run tests in container
docker-compose exec web pytest
```

---

## 📋 Git Workflow

### Branch Naming
```
feature/description      # New features
fix/description         # Bug fixes
docs/description        # Documentation
release/version         # Release branches
```

### Commit Message Format
```
Type: Brief description

- Detailed explanation (optional)
- Additional context (optional)

Fixes #123
```

### Example
```
feat: Add JWT authentication

- Implement token generation and validation
- Add refresh token mechanism
- Include comprehensive tests

Fixes #45
```

---

## 📝 Pull Request Checklist

Before submitting a PR:

- [ ] Branch is up-to-date with main
- [ ] All tests passing (`pytest`)
- [ ] Code formatted (`black`)
- [ ] Linting pass (`ruff check`)
- [ ] Type checking pass (`mypy`)
- [ ] Coverage maintained (80%+)
- [ ] Documentation updated
- [ ] No hardcoded values or secrets
- [ ] Commits are clean and descriptive

---

## 🔍 Code Review Guidelines

### Reviewer Checklist

- [ ] Changes align with architecture
- [ ] Tests are comprehensive
- [ ] No security vulnerabilities
- [ ] Code style consistent
- [ ] Documentation adequate
- [ ] Performance implications considered
- [ ] No unnecessary dependencies
- [ ] Backward compatible

---

## 🔐 Security Reminders

⚠️ **NEVER**:
- Commit `.env` files with secrets
- Hardcode API keys or passwords
- Log sensitive information
- Skip security checks
- Use eval() or similar unsafe functions
- Trust user input without validation

✅ **ALWAYS**:
- Use environment variables for secrets
- Validate and sanitize input
- Use parameterized queries
- Keep dependencies updated
- Enable HTTPS in production
- Review security implications
- Use strong encryption

---

## 📊 Testing Pyramid

Maintain this distribution:

```
         /\
        /E2E\          5-10%  (End-to-end tests)
       /------\
      /Integra.\       10-20% (Integration tests)
     /----------\
    /Unit Tests \      70-80% (Unit tests)
   /____________\
```

---

## 📦 Directory Quick Reference

| Directory | Create Files Here When... |
|-----------|---------------------------|
| `src/` | Building application features |
| `tests/` | Writing test cases |
| `docs/` | Creating user-facing documentation |
| `architecture/` | Documenting technical decisions |
| `docker/` | Adding container configuration |
| `deployment/` | Adding infrastructure code |
| `scripts/` | Creating operational scripts |
| `postman/` | Adding API test collections |
| `.github/` | Setting up automation workflows |

---

## 🐛 Debugging Tips

### Django Debug
```python
from django.shortcuts import debugger
debugger()  # Sets breakpoint
```

### Print Debugging
```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Value: %s", value)
```

### Django Shell
```bash
python manage.py shell

# In shell:
from src.models import User
User.objects.all()
User.objects.filter(email='user@example.com').first()
```

### Database Queries
```python
from django.db import connection
connection.queries  # View executed queries
```

---

## 🆘 Common Issues

### ModuleNotFoundError
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Database Connection
```bash
# Check PostgreSQL is running
psql -V

# Verify DATABASE_URL in .env
```

### Tests Failing
```bash
# Clear cache
find . -type d -name __pycache__ -exec rm -r {} +
rm -rf .pytest_cache

# Reset database
python manage.py migrate
```

---

## 📚 Learning Resources

### Django
- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)

### Testing
- [Pytest Documentation](https://docs.pytest.org/)
- [Testing Best Practices](https://en.wikipedia.org/wiki/Software_testing)

### Architecture
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

### DevOps
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

---

## 🤝 Getting Help

1. Check [STRUCTURE.md](STRUCTURE.md) for file organization
2. Read relevant documentation in `docs/` or `architecture/`
3. Search GitHub issues for similar problems
4. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details

---

## 📞 Contact & Support

- **Project Lead**: [Your Name]
- **Documentation**: See `docs/` directory
- **Architecture**: See `architecture/` directory
- **Issues**: GitHub Issues
- **PRs**: GitHub Pull Requests

---

**Last Updated**: 2024
**Version**: 1.0.0
**Status**: Production Ready Foundation
