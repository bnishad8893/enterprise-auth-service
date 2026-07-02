# Development Helper Scripts

Quick reference for development automation scripts.

## Available Scripts

### setup.sh
Initializes the development environment.

```bash
./scripts/setup.sh
```

**What it does:**
- Validates Python 3.13
- Installs/upgrades uv
- Creates virtual environment
- Installs all dependencies (dev, test, docs)
- Sets up pre-commit hooks
- Creates .env file from template

**When to use:** First time setup or when reinitializing the environment.

---

### format.sh
Formats Python code using Ruff.

```bash
./scripts/format.sh [src|tests|all]
./scripts/format.sh all        # Format all Python code
./scripts/format.sh src        # Format only src/
./scripts/format.sh tests      # Format only tests/
```

**What it does:**
- Auto-formats Python code to project standards
- Sorts imports
- Fixes simple style issues

**When to use:** Before committing code or as part of CI/CD.

---

### lint.sh
Runs code quality checks (Ruff + MyPy).

```bash
./scripts/lint.sh
```

**What it does:**
- Runs Ruff linter with all rules enabled
- Checks code formatting
- Performs strict type checking with MyPy
- Reports all issues

**When to use:** Before pushing code to ensure quality standards.

**Note:** Issues are reported but not auto-fixed. Use:
- `ruff check --fix` to auto-fix Ruff issues
- `./scripts/format.sh` to fix formatting
- MyPy issues require manual fixes

---

### test.sh
Runs pytest with coverage reporting.

```bash
./scripts/test.sh                    # Run all tests with coverage
./scripts/test.sh unit              # Run only unit tests
./scripts/test.sh integration       # Run only integration tests
./scripts/test.sh --cov            # Include coverage report
./scripts/test.sh --verbose        # Verbose output
./scripts/test.sh --fast           # Skip slow tests
```

**What it does:**
- Discovers and runs all tests
- Generates coverage reports (HTML + terminal)
- Displays test results
- Fails if coverage drops below threshold (80%)

**Coverage output:**
- Terminal: Summary with missing line numbers
- HTML report: `htmlcov/index.html`
- XML: `coverage.xml` (for CI/CD integration)

**When to use:** After writing code or before commits.

---

### run.sh
Starts the development server and services.

```bash
./scripts/run.sh server             # Start Django dev server
./scripts/run.sh worker             # Start Celery worker
./scripts/run.sh beat               # Start Celery Beat scheduler
./scripts/run.sh all                # Instructions for all services
```

**Server:**
- Django development server on http://localhost:8000
- Hot-reload enabled

**Worker:**
- Celery task worker for async jobs

**Beat:**
- Celery scheduler for periodic tasks

**When to use:** Running the application locally.

---

## Quick Workflow

### First Time Setup
```bash
./scripts/setup.sh
source .venv/bin/activate
./scripts/run.sh server
```

### Before Committing
```bash
./scripts/format.sh
./scripts/lint.sh
./scripts/test.sh
```

### During Development
```bash
# Terminal 1: Development server
./scripts/run.sh server

# Terminal 2: Run tests on changes
pytest --watch tests/

# Terminal 3: Code quality checks
./scripts/lint.sh
```

---

## Advanced Usage

### Running specific tests
```bash
pytest tests/unit/test_auth.py::TestLoginFlow::test_success
```

### Coverage with specific modules
```bash
./scripts/test.sh --cov src.auth src.models
```

### Pre-commit hooks
Pre-commit hooks are configured automatically and run on commit:
```bash
# Run all hooks manually
pre-commit run --all-files

# Skip hooks for emergency commits (not recommended)
git commit --no-verify
```

---

## Troubleshooting

### Virtual environment not activating?
```bash
source .venv/bin/activate
```

### Dependencies outdated?
```bash
./scripts/setup.sh
```

### Tests failing due to database?
```bash
# PostgreSQL must be running (via docker-compose)
docker-compose up -d db
```

### MyPy errors you disagree with?
Add type ignores carefully (marked for review by team):
```python
result: SomeType = function()  # type: ignore[assignment]
```

---

## Documentation

- [SETUP_GUIDE.md](../docs/SETUP_GUIDE.md) - Detailed development setup
- [DEVELOPER_GUIDE.md](../docs/DEVELOPER_GUIDE.md) - Coding standards
- [pyproject.toml](../pyproject.toml) - Dependencies and configuration
