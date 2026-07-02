# Enterprise Auth Service

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Code Quality](https://img.shields.io/badge/code%20quality-strict-brightgreen.svg)](pyproject.toml)

A production-ready Authentication & User Management API built with Django, Django REST Framework, PostgreSQL, Redis, JWT, OAuth2, and modern DevOps practices.

## 🎯 Project Status

✅ **Foundation Phase Complete**
- Python 3.13 environment configured with uv
- Enterprise-grade code quality tools (Ruff, MyPy, Pytest)
- Production-ready Docker & Docker Compose setup
- CI/CD pipeline with GitHub Actions
- Development environment fully automated

🚧 **Next Phase** - Django models, API endpoints, authentication logic

## 🏗️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Runtime** | Python 3.13 |
| **Package Manager** | uv |
| **Framework** | Django 5.0+ |
| **API** | Django REST Framework |
| **Database** | PostgreSQL 16 |
| **Cache/Broker** | Redis 7 |
| **Async Tasks** | Celery |
| **Type Checking** | MyPy (strict) |
| **Linting** | Ruff |
| **Testing** | Pytest |
| **Containerization** | Docker + Docker Compose |
| **CI/CD** | GitHub Actions |

##  ⚡ Quick Start (5 minutes)

```bash
# Clone and setup
git clone https://github.com/yourusername/enterprise-auth-service.git
cd enterprise-auth-service

# Automated setup (Python 3.13 + all tools)
./scripts/setup.sh

# Activate environment
source .venv/bin/activate

# Start development server
./scripts/run.sh server
```

🎉 **Application running at http://localhost:8000**

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [Quick Start](QUICK_START.md) | 5-minute quick reference |
| [Setup Guide](docs/SETUP_GUIDE.md) | Complete development setup |
| [Developer Guide](docs/DEVELOPER_GUIDE.md) | Coding standards and practices |
| [API Documentation](docs/API_DOCUMENTATION.md) | REST API specification |
| [System Design](architecture/SYSTEM_DESIGN.md) | Architecture overview |
| [Database Design](architecture/DATABASE_DESIGN.md) | Database schema |
| [Security Architecture](architecture/SECURITY_ARCHITECTURE.md) | Security model |
| [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) | Production deployment |
| [Scripts Reference](scripts/README.md) | Helper scripts documentation |

## 🚀 Development Workflow

### Essential Commands

```bash
# Format code
./scripts/format.sh

# Run quality checks (Ruff + MyPy)
./scripts/lint.sh

# Run tests with coverage
./scripts/test.sh

# Start development server
./scripts/run.sh server

# Start Celery worker
./scripts/run.sh worker
```

### Automated CI/CD

Every push/PR triggers:
- ✅ Ruff linting and formatting
- ✅ MyPy strict type checking
- ✅ Pytest with 80% coverage requirement
- ✅ Pre-commit hooks validation

## 🏗️ Project Structure

```
enterprise-auth-service/
├── src/                      # Application source code
│   └── settings.py          # Django settings (to be created)
├── tests/                   # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── docs/                   # Documentation
│   ├── SETUP_GUIDE.md
│   ├── DEVELOPER_GUIDE.md
│   └── API_DOCUMENTATION.md
├── scripts/                # Helper scripts
│   ├── setup.sh           # Environment setup
│   ├── format.sh          # Code formatting
│   ├── lint.sh            # Quality checks
│   ├── test.sh            # Run tests
│   └── run.sh             # Start services
├── .github/
│   └── workflows/ci.yml   # CI/CD pipeline
├── .devcontainer/         # Dev container config
├── Dockerfile             # Production image
├── docker-compose.yml     # Local development
├── pyproject.toml         # Dependencies & config
├── .pre-commit-config.yaml # Git hooks
└── .env.example           # Environment template
```

## 🛠️ Code Quality Standards

| Aspect | Standard |
|--------|----------|
| **Python Version** | 3.13 minimum |
| **Type Hints** | Required (enforced by MyPy strict) |
| **Code Format** | Ruff format |
| **Linting** | Ruff all checks enabled |
| **Test Coverage** | 80% minimum |
| **Line Length** | 100 characters |
| **Imports** | Sorted by Ruff |
| **Pre-commit** | Enforced on all commits |

## 🐳 Docker & Containerization

### Production Dockerfile
- Multi-stage build for minimal image size
- Non-root user for security
- Health checks enabled
- Optimized Gunicorn configuration

### Docker Compose
Services included:
- `app` - Django application
- `db` - PostgreSQL database
- `cache` - Redis cache
- `pgadmin` - Database management (optional)
- `celery_worker` - Async task worker (optional)
- `celery_beat` - Task scheduler (optional)

```bash
# Start all services
docker-compose up

# Start with background mode
docker-compose up -d

# Access services
# App: http://localhost:8000
# pgAdmin: http://localhost:5050
```

## 📊 Configuration

### Environment Variables

Critical `.env` configuration:
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

See [`.env.example`](.env.example) for complete configuration options.

## 🔍 Quality Tools

### Ruff Configuration
Includes all rule categories:
- Pyflakes (F)
- Pycodestyle (E, W)
- isort (I)
- pyupgrade (UP)
- Security (S)
- Type checking (TCH)
- Complexity analysis (C901)

### MyPy Configuration
- Strict mode enabled
- Disallow untyped defs
- No implicit optional
- Warn unused ignores

### Pytest Configuration
- Test discovery in `tests/`
- Coverage reporting (HTML + XML)
- Coverage threshold: 80%
- Async test support
- Markers: unit, integration, slow, database, async

## 🔐 Security

- Non-root Docker user
- Health checks for all services
- Type safety with MyPy
- Security linting with Ruff
- Pre-commit hooks for git integrity
- Environment variable isolation
- Docker security best practices

## 📦 Dependencies

Managed via **uv** with organized groups:
- `production` - Django, DRF, PostgreSQL, Redis, Celery
- `dev` - Code quality tools (Ruff, MyPy, Black)
- `test` - Testing frameworks (Pytest, Factory Boy)
- `docs` - Documentation tools (Sphinx)

Install with:
```bash
uv pip install -e ".[dev,test]"
```

## 🚀 Getting Started

### First Time Setup
```bash
./scripts/setup.sh
source .venv/bin/activate
./scripts/run.sh server
```

### Development Workflow
```bash
# Format
./scripts/format.sh

# Check quality
./scripts/lint.sh

# Test
./scripts/test.sh

# Commit
git add .
git commit -m "feat: description"
```

### Using Dev Container
1. Open in VS Code
2. Install "Dev Containers" extension
3. Press `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"
4. Tools auto-configured inside container

## 🤝 Contributing

Please see [Developer Guide](docs/DEVELOPER_GUIDE.md) for:
- Code style requirements
- Testing standards
- Git workflow
- Pull request process
- Type hint guidelines

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## 📞 Support

- **Documentation**: [See docs/](docs/)
- **Quick Reference**: [QUICK_START.md](QUICK_START.md)
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

---

**Built with ❤️ following enterprise-grade engineering practices**

## Deployment

Deployment procedures and infrastructure configurations are in the [deployment/](deployment/) directory.

Supported platforms:
- Kubernetes
- Docker Compose
- AWS ECS
- AWS Lambda
- GCP Cloud Run
- Azure Container Instances

## Monitoring & Observability

- Structured logging
- Distributed tracing
- Metrics collection
- Health checks and readiness probes
- Error tracking and alerting

## Security

- JWT token management
- OAuth2 integration
- Rate limiting
- CORS configuration
- HTTPS enforcement
- Secrets management

See [architecture/SECURITY_ARCHITECTURE.md](architecture/SECURITY_ARCHITECTURE.md) for detailed security architecture.

## Performance

Optimized for high-throughput scenarios with:
- Redis caching
- Database query optimization
- Asynchronous task processing
- Connection pooling

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Enterprise Support

For enterprise deployments, support services, and consulting, please contact the project maintainers.

## Maintainers

- Project Owner: [Your Name/Organization]

---

**Built with professional engineering standards for production use.**
