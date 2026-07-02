# Development Setup Guide

Complete guide for setting up the Enterprise Auth Service development environment.

## Prerequisites

**Required:**
- Python 3.13 (verified with `.python-version`)
- git
- Docker & Docker Compose (for containerized services)

**Recommended:**
- VS Code with Dev Containers extension
- 8GB+ RAM
- 10GB+ disk space for dependencies and database

## Installation

### Option 1: Automated Setup (Recommended)

Fastest way to get started with all tools pre-configured:

```bash
# Clone repository
git clone https://github.com/yourusername/enterprise-auth-service.git
cd enterprise-auth-service

# Run automated setup
./scripts/setup.sh

# Activate virtual environment
source .venv/bin/activate

# Copy and edit environment configuration
cp .env.example .env
# Edit .env with your database credentials and settings
```

The setup script will:
- Create Python 3.13 virtual environment with uv
- Install all dependencies (production, development, testing)
- Configure pre-commit hooks for code quality
- Create necessary directories
- Generate .env file from template

### Option 2: Manual Setup

For more control over the installation:

```bash
# Create virtual environment
python3.13 -m venv .venv
source .venv/bin/activate

# Upgrade pip and install uv
pip install --upgrade pip uv

# Install project dependencies
uv pip install -e ".[dev,test]"

# Set up pre-commit hooks
pre-commit install

# Create environment configuration
cp .env.example .env
# Edit .env with your settings
```

### Option 3: Docker & Dev Containers

For a complete containerized development environment:

1. Open project in VS Code
2. Install "Dev Containers" extension
3. Press `Ctrl+Shift+P` and run "Dev Containers: Reopen in Container"
4. Wait for container to build and start
5. Run `./scripts/setup.sh` inside container

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and update with your settings:

```bash
cp .env.example .env
```

**Critical settings:**
```env
# Django
DEBUG=False                    # Set to False in production
SECRET_KEY=your-secret-key    # Generate random key in production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/enterprise_auth_dev
POSTGRES_PASSWORD=postgres

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1

# Email (for local testing)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password

# Security
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Services (optional for now)
SENTRY_DSN=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

See `.env.example` for complete configuration options.

## Database Setup

### Using Docker Compose (Recommended)

```bash
# Start PostgreSQL and Redis services
docker-compose up -d db cache

# Wait for services to be healthy
docker-compose logs db    # Check PostgreSQL
docker-compose logs cache # Check Redis
```

### Local PostgreSQL

If running PostgreSQL locally:

```bash
# Create database
createdb enterprise_auth_dev

# Create user
createuser -P -d postgres

# Ensure user has permissions
psql enterprise_auth_dev -c "GRANT ALL ON SCHEMA public TO postgres;"
```

## Dependency Management

This project uses **uv** for fast, reliable Python dependency management.

### Installing Dependencies

```bash
# All dependencies
uv pip install -e ".[dev,test]"

# Production only
uv pip install -e "."

# Development tools
uv pip install -e ".[dev]"

# Testing tools
uv pip install -e ".[test]"

# Documentation
uv pip install -e ".[docs]"

# All combinations
uv pip install -e ".[dev,test,docs]"
```

### Updating Dependencies

```bash
# Check for updates
uv pip list --outdated

# Update specific package
uv pip install --upgrade django

# Rebuild lock file
uv pip compile pyproject.toml > requirements.lock
```

## Code Quality Tools

### Ruff - Linting & Formatting

```bash
# Format code
./scripts/format.sh
# or
ruff format src/ tests/

# Check for issues
./scripts/lint.sh
# or
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/
```

### MyPy - Type Checking

```bash
# Run type checker
mypy src/ --strict --ignore-missing-imports

# Type check specific file
mypy src/auth/__init__.py
```

### Pre-commit Hooks

Hooks run automatically before each commit:

```bash
# Run all hooks manually
pre-commit run --all-files

# Update hook versions
pre-commit autoupdate

# Bypass hooks (use carefully!)
git commit --no-verify
```

## Testing

### Running Tests

```bash
# All tests
./scripts/test.sh

# Specific test file
pytest tests/unit/test_auth.py -v

# Specific test class
pytest tests/unit/test_auth.py::TestLogin -v

# Specific test method
pytest tests/unit/test_auth.py::TestLogin::test_success -v

# Filtered by marker
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests

# With coverage
pytest --cov=src --cov-report=html

# Continue on first failure
pytest -x
```

### Coverage Reports

```bash
# Terminal report
./scripts/test.sh

# HTML report
open htmlcov/index.html

# Coverage threshold check
pytest --cov=src --cov-fail-under=80
```

## Running the Application

### Development Server

```bash
# Quick start
./scripts/run.sh server

# With debug logging
DEBUG=True ./scripts/run.sh server

# Custom port
python manage.py runserver 0.0.0.0:9000
```

Server runs on http://localhost:8000

### Using Docker Compose

```bash
# Start all services
docker-compose up

# In another terminal, create superuser
docker-compose exec app python manage.py createsuperuser

# Access on http://localhost:8000
```

### With Async Tasks (Celery)

```bash
# Terminal 1: Web server
./scripts/run.sh server

# Terminal 2: Celery worker
./scripts/run.sh worker

# Terminal 3: Celery Beat scheduler
./scripts/run.sh beat
```

## Debugging

### Using Python Debugger

```python
# In your code
import pdb; pdb.set_trace()

# Or use breakpoint (Python 3.7+)
breakpoint()
```

### Using VS Code Debugger

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django",
      "type": "python",
      "request": "launch",
      "module": "django",
      "args": ["runserver"],
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}",
          "remoteRoot": "."
        }
      ]
    }
  ]
}
```

### Database Debugging

```bash
# Access PostgreSQL directly
psql enterprise_auth_dev

# List tables
\dt

# View table schema
\d+ table_name

# Using pgAdmin (via Docker)
# http://localhost:5050
# Email: admin@localhost
# Password: admin
```

## Troubleshooting

### Python Version Mismatch

```bash
# Verify Python version
python --version

# Install Python 3.13 with pyenv
pyenv install 3.13.0
pyenv local 3.13.0
```

### Virtual Environment Issues

```bash
# Remove and recreate
rm -rf .venv/
uv venv .venv
source .venv/bin/activate

# Or run setup
./scripts/setup.sh
```

### Database Connection Errors

```bash
# Check PostgreSQL is running
docker-compose exec db pg_isready

# Reset database
docker-compose down -v  # Remove volumes
docker-compose up -d db

# Check connection string in .env
# Format: postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

### Pre-commit Hook Failures

```bash
# Fix issues automatically
ruff check --fix
ruff format

# Run pre-commit again
pre-commit run --all-files

# Force commit if urgent (not recommended)
git commit --no-verify
```

### Dependency Conflicts

```bash
# Clear pip cache
pip cache purge

# Reinstall from scratch
rm -rf .venv/
./scripts/setup.sh

# Check for outdated packages
uv pip list --outdated
```

## IDE Setup

### VS Code

Extensions (auto-installed with Dev Container):
- Python
- Pylance
- Ruff
- MyPy Type Checker
- Docker
- GitLens
- REST Client

### PyCharm Professional

Settings:
- Python Interpreter: Project > Python 3.13 venv
- Code Style: 100-char line length
- VCS > Git > Hooks: Enable pre-commit

## Performance Tips

- Use `django-extensions` for faster shell:
  ```bash
  pip install django-extensions
  python manage.py shell_plus
  ```

- Run tests in parallel:
  ```bash
  pytest -n auto
  ```

- Use Django Debug Toolbar:
  ```bash
  pip install django-debug-toolbar
  ```

## Next Steps

1. ✅ Environment configured
2. 📚 Read [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
3. 📖 Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
4. 🏗️ Review [SYSTEM_DESIGN.md](../architecture/SYSTEM_DESIGN.md)
5. 🚀 Start developing!

## Getting Help

- **Errors in setup**: Check error message in terminal
- **Dependency issues**: Run `./scripts/setup.sh` again
- **Database problems**: Check PG logs with `docker-compose logs db`
- **Code quality**: Run `./scripts/lint.sh` for suggestions
- **Documentation**: See [README.md](../README.md) for overview

## Related Documentation

- [QUICK_START.md](../QUICK_START.md) - Quick command reference
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - Coding standards
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Production deployment
- [scripts/README.md](../scripts/README.md) - Helper scripts
python manage.py migrate
```

Create a new migration:

```bash
python manage.py makemigrations
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_auth.py
```

## Code Quality Checks

```bash
# Format code with Black
black src/ tests/

# Lint with Ruff
ruff check src/ tests/

# Type checking with MyPy
mypy src/
```

## Common Issues

### PostgreSQL Connection Error

Verify PostgreSQL is running and connection string is correct in `.env`.

### Redis Connection Error

Ensure Redis is running: `redis-cli ping` should return `PONG`.

### Migration Conflicts

Reset database (development only):

```bash
python manage.py flush
python manage.py migrate
```

## Next Steps

- Read [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API reference
- Check [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for coding standards
- Review [architecture/SYSTEM_DESIGN.md](../architecture/SYSTEM_DESIGN.md) for system design

## Troubleshooting

For detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
