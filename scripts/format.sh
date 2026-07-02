#!/bin/bash
# format.sh - Format Python code using Ruff
# Usage: ./scripts/format.sh [src|tests|all]
# If no argument provided, formats all Python files

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    source .venv/bin/activate
fi

echo -e "${YELLOW}Formatting Python code with Ruff...${NC}"

# Determine which files to format
TARGET="${1:-all}"

case $TARGET in
    src)
        echo "Formatting src/ directory..."
        ruff format src/
        ;;
    tests)
        echo "Formatting tests/ directory..."
        ruff format tests/
        ;;
    all)
        echo "Formatting all Python files..."
        ruff format .
        ;;
    *)
        echo "Unknown target: $TARGET"
        echo "Usage: $0 [src|tests|all]"
        exit 1
        ;;
esac

echo -e "${GREEN}✓ Code formatting complete${NC}"
