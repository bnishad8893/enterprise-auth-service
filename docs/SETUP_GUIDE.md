# Setup Guide

This guide covers local development environment setup and installation procedures.

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 14 or higher
- Redis 7 or higher
- Docker and Docker Compose (optional, for containerized setup)
- Git

## Installation Methods

### Option 1: Docker Compose (Recommended)

The fastest way to get started with all services running.

```bash
# Clone the repository
git clone https://github.com/yourusername/enterprise-auth-service.git
cd enterprise-auth-service

# Start services
docker-compose up -d

# Initialize database
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

Access the application at `http://localhost:8000`.

### Option 2: Local Python Environment

For development without Docker.

#### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

#### 4. Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

#### 5. Run Development Server

```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`.

### Option 3: VS Code Dev Container

For a consistent development environment with all tools pre-configured.

1. Open the project in VS Code
2. Install the "Dev Containers" extension
3. Click the green button in the bottom-left and select "Reopen in Container"
4. Wait for the container to build
5. Terminal access will be inside the container with all tools ready

## Environment Configuration

Key environment variables:

- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Django secret key (generate a new one for production)
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `CORS_ALLOWED_ORIGINS`: CORS whitelist

## Database Migrations

Run migrations after pulling code changes:

```bash
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
