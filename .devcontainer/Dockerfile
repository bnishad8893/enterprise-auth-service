# Development Container - Based on Official Python 3.13 DevContainer
FROM mcr.microsoft.com/devcontainers/python:3.13

# Install additional system dependencies for development
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    redis-tools \
    curl \
    git \
    build-essential \
    libpq-dev \
    postgresql \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir uv

# Create a non-root user workspace
RUN usermod -s /bin/bash vscode || true

# Pre-create virtual environment directory
RUN mkdir -p /workspace/.venv && \
    chown -R vscode:vscode /workspace

USER vscode
