# Multi-stage Docker build for minimal production image size
# Stage 1: Builder
FROM python:3.13-slim as builder

# Set working directory
WORKDIR /build

# Install system build dependencies only in builder stage
RUN apt-get update && apt-cache search postgresql-client && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install uv in builder
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv

# Install Python dependencies into a virtual environment
RUN uv venv /build/venv && \
    /build/venv/bin/uv pip install --no-cache-dir .

# Stage 2: Runtime
FROM python:3.13-slim

# Set metadata
LABEL maintainer="Enterprise Auth Team"
LABEL description="Enterprise Auth Service - Production Docker Image"
LABEL version="0.1.0"

# Security: Create non-root user for running the application
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=src.settings \
    PORT=8000

# Set working directory
WORKDIR /app

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /build/venv /app/venv

# Copy application code
COPY --chown=appuser:appuser . .

# Create required directories for application
RUN mkdir -p /app/logs /app/media /app/static && \
    chown -R appuser:appuser /app

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health/ || exit 1

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE ${PORT}

# Production startup command using Gunicorn with optimized settings
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--worker-tmp-dir", "/dev/shm", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "--access-log-format", "%(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\"", \
     "src.wsgi:application"]
