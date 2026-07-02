# Source Code

This directory contains all application source code.

## Structure

- **core/**: Core business logic and domain models
- **api/**: REST API endpoints and serializers
- **services/**: Service layer for business operations
- **models/**: Database models and schemas
- **auth/**: Authentication and authorization logic
- **middleware/**: Custom middleware components
- **utils/**: Utility functions and helpers
- **config/**: Application configuration management
- **celery_tasks/**: Asynchronous task definitions

## Design Principles

- **Clean Architecture**: Separation of concerns across layers
- **Domain-Driven Design**: Business logic independent from frameworks
- **SOLID Principles**: Maintainable and testable code
- **Single Responsibility**: Each module has one reason to change

## Guidelines

- All code follows PEP 8 style guidelines
- Type hints are required for all functions
- Business logic is isolated from framework code
- External dependencies are abstracted through interfaces
