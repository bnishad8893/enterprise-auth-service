# Docker

This directory contains Docker configuration files and Dockerfiles.

## Structure

- **Dockerfile**: Main application container image
- **Dockerfile.test**: Container for running tests
- **docker-compose.yml**: Multi-container orchestration for development
- **docker-compose.prod.yml**: Production-like container configuration
- **entrypoint.sh**: Container startup script
- **.dockerignore**: Files to exclude from Docker builds

## Purpose

Provides reproducible, containerized environments for:
- Local development (Docker Compose)
- Testing (isolated test environment)
- Production deployment (optimized images)
- CI/CD pipelines (consistent build environment)

## Best Practices

- Images are kept minimal and efficient
- No unnecessary layers or dependencies
- Secrets are injected at runtime, never baked in
- Health checks are defined for production containers
- Images follow security best practices
