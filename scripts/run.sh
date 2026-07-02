#!/bin/bash
# run.sh - Start the development server
# Usage: ./scripts/run.sh [server|worker|beat|all]

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    source .venv/bin/activate
fi

# Load environment variables
if [ -f .env ]; then
    set -a
    source .env
    set +a
else
    echo -e "${RED}✗ .env file not found. Copy from .env.example and update.${NC}"
    exit 1
fi

echo -e "${YELLOW}Enterprise Auth Service - Development Server${NC}\n"

# Determine what to run
SERVICE="${1:-server}"

case $SERVICE in
    server)
        echo -e "${YELLOW}Starting Django development server...${NC}"
        echo "Listening on http://0.0.0.0:8000"
        echo "Press Ctrl+C to stop"
        python manage.py runserver 0.0.0.0:8000
        ;;
    worker)
        echo -e "${YELLOW}Starting Celery worker...${NC}"
        celery -A src worker -l info
        ;;
    beat)
        echo -e "${YELLOW}Starting Celery Beat scheduler...${NC}"
        celery -A src beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
        ;;
    all)
        echo -e "${YELLOW}Starting all services (requires multiple terminals)${NC}"
        echo "Run each command in a separate terminal:"
        echo "  ./scripts/run.sh server"
        echo "  ./scripts/run.sh worker"
        echo "  ./scripts/run.sh beat"
        ;;
    *)
        echo "Unknown service: $SERVICE"
        echo "Usage: $0 [server|worker|beat|all]"
        exit 1
        ;;
esac
