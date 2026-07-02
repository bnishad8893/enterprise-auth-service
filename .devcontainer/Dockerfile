# Dev Container Dockerfile
# Built from official Python image for consistency
FROM mcr.microsoft.com/devcontainers/python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    redis-tools \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Development dependencies will be installed via pip
# See requirements-dev.txt for list
