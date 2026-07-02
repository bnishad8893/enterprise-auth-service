# Quick Reference Guide

Essential commands and resources for developing in this repository.

## � Quick Start (5 minutes)

```bash
# 1. Clone and navigate
git clone https://github.com/yourusername/enterprise-auth-service.git
cd enterprise-auth-service

# 2. Automated setup (Python 3.13 + dependencies + pre-commit)
./scripts/setup.sh

# 3. Activate environment
source .venv/bin/activate

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Start services (multiple terminals)
# Terminal 1: Start application
./scripts/run.sh server

# Terminal 2: Start Celery worker (optional)
./scripts/run.sh worker
```

Application running at **http://localhost:8000**

---

## 📖 Documentation Quick Links

### Getting Started
- [Setup Guide](docs/SETUP_GUIDE.md) - Complete development setup
- [Developer Guide](docs/DEVELOPER_GUIDE.md) - Coding standards and practices
- [scripts/README.md](scripts/README.md) - Helper scripts documentation

### Architecture & Design
- [System Design](architecture/SYSTEM_DESIGN.md) - System architecture
- [Database Design](architecture/DATABASE_DESIGN.md) - Database schema
- [Security Architecture](architecture/SECURITY_ARCHITECTURE.md) - Security model
- [Architecture Decisions](docs/ARCHITECTURE_DECISIONS.md) - ADRs

### Operations
- [API Documentation](docs/API_DOCUMENTATION.md) - REST API spec
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Production deployment
- [Project Structure](planning/STRUCTURE.md) - Directory organization

---

## 🛠️ Essential Commands

### Environment Setup
```bash
# Initial setup (run once)
./scripts/setup.sh

# Activate virtual environment
source .venv/bin/activate

# Show Python version
python --version

# List installed packages
uv pip list
```

### Code Quality & Formatting
```bash
# Format code automatically
./scripts/format.sh

# Format specific directory
./scripts/format.sh src
./scripts/format.sh tests

# Check code quality (Ruff + MyPy)
./scripts/lint.sh

# Auto-fix linting issues
ruff check --fix src/ tests/
```

### Testing & Coverage
```bash
# Run all tests
./scripts/test.sh

# Run unit tests only
pytest -m unit

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_auth.py::TestLogin::test_success -v

# Run tests matching pattern
pytest -k "test_auth" -v

# Coverage report (HTML)
open htmlcov/index.html
```

### Development Server
```bash
# Start Django development server
./scripts/run.sh server

# Start Celery worker for async tasks
./scripts/run.sh worker

# Start Celery Beat scheduler
./scripts/run.sh beat

# Run management commands
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
```

### Database
```bash
# Start PostgreSQL and Redis via Docker
docker-compose up -d db cache

# Access PostgreSQL
psql enterprise_auth_dev

# Access pgAdmin
# Open http://localhost:5050
# Email: admin@localhost, Password: admin
```

### Pre-commit Hooks
```bash
# Run all hooks manually
pre-commit run --all-files

# Install/update hooks
pre-commit install
pre-commit autoupdate

# Bypass hooks (emergency only!)
git commit --no-verify
```

### Dependency Management
```bash
# Install dependencies
uv pip install -e ".[dev,test]"

# Check for outdated packages
uv pip list --outdated

# Update specific package
uv pip install --upgrade django

# Install from requirements
uv pip install -r requirements.txt
```

---

## 🔄 Development Workflow

### Before Starting Work
```bash
source .venv/bin/activate
git pull
./scripts/setup.sh  # If dependencies changed
```

### During Development
```bash
# Terminal 1: Dev server
./scripts/run.sh server

# Terminal 2: Watch tests (install pytest-watch first)
pip install pytest-watch
ptw tests/ -- --cov=src

# Terminal 3: Run linting on changes
./scripts/lint.sh
```

### Before Committing
```bash
# Format code
./scripts/format.sh

# Check quality
./scripts/lint.sh

# Run all tests
./scripts/test.sh

# Run pre-commit hooks
pre-commit run --all-files

# Then commit
git add .
git commit -m "feat: description of changes"
```

### After Pulling Changes
```bash
source .venv/bin/activate
git pull

# Update dependencies if pyproject.toml changed
./scripts/setup.sh

# Run migrations if database changed
python manage.py migrate

# Run tests to verify everything
./scripts/test.sh
```

---

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up

# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f app
docker-compose logs -f db
docker-compose logs -f cache

# Stop all services
docker-compose down

# Stop and remove volumes (reset database)
docker-compose down -v

# Run command in container
docker-compose exec app python manage.py createsuperuser

# Rebuild image
docker-compose build --no-cache
```

---

## 📊 Environment Variables

Critical `.env` variables (see `.env.example` for complete list):

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/enterprise_auth_dev

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
```

---

## 🐛 Troubleshooting

### Virtual Environment Not Found
```bash
python3.13 -m venv .venv
source .venv/bin/activate
uv pip install -e ".[dev,test]"
```

### Database Connection Failed
```bash
docker-compose up -d db cache
docker-compose logs db
```

### Tests Failing
```bash
# Reinstall dependencies
./scripts/setup.sh

# Reset database
docker-compose restart db
pytest --no-cov -v
```

### Pre-commit Hook Errors
```bash
# Auto-fix issues
ruff check --fix
ruff format

# Run hooks again
pre-commit run --all-files
```

### Module Not Found Errors
```bash
# Reinstall package in editable mode
uv pip install -e ".[dev,test]"

# Verify installation
python -c "import src; print(src.__file__)"
```

---

## 📚 Key Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project config, dependencies, tool settings |
| `.env.example` | Environment variable template |
| `.pre-commit-config.yaml` | Git hooks configuration |
| `docker-compose.yml` | Services configuration |
| `Dockerfile` | Production Docker image |
| `.devcontainer/devcontainer.json` | Dev container config |
| `.github/workflows/ci.yml` | CI/CD pipeline |

---

## 🎯 Tool Versions

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.13 | Application runtime |
| Django | 5.0+ | Web framework |
| PostgreSQL | 16 | Main database |
| Redis | 7 | Cache & broker |
| Docker | Latest | Containerization |
| Ruff | 0.4.1+ | Linting & formatting |
| MyPy | 1.11.0+ | Type checking |
| Pytest | 7.4+ | Testing framework |

---

## 💡 Tips

- **Fast code checks**: `ruff check --fix` before committing
- **Run tests faster**: `pytest -n auto` (requires pytest-xdist)
- **Debug in IDE**: Set breakpoints in VS Code
- **Hot reload**: Dev server automatically reloads on file changes
- **Database in container**: Use Docker Compose for consistency

---

## More Information

- 📖 [Complete Setup Guide](docs/SETUP_GUIDE.md)
- 🏗️ [Architecture](architecture/SYSTEM_DESIGN.md)
- 🔗 [API Docs](docs/API_DOCUMENTATION.md)
- 🚀 [Deployment](docs/DEPLOYMENT_GUIDE.md)

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
