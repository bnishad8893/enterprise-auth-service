#!/bin/bash
# lint.sh - Run code quality checks (Ruff + MyPy)
# Usage: ./scripts/lint.sh [check|fix|all]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    source .venv/bin/activate
fi

echo -e "${YELLOW}Running code quality checks...${NC}\n"

FAIL_COUNT=0

# Parse arguments
ACTION="${1:-all}"

# Ruff linting
echo -e "${YELLOW}1. Ruff - Linting and import sorting${NC}"
if ruff check src/ tests/ --show-fixes; then
    echo -e "${GREEN}✓ Ruff linting passed${NC}\n"
else
    echo -e "${RED}✗ Ruff linting found issues (run 'ruff check --fix' to auto-fix)${NC}\n"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Ruff format check
echo -e "${YELLOW}2. Ruff - Format check${NC}"
if ruff format --check src/ tests/; then
    echo -e "${GREEN}✓ Ruff format check passed${NC}\n"
else
    echo -e "${RED}✗ Format issues found (run './scripts/format.sh' to fix)${NC}\n"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# MyPy type checking
echo -e "${YELLOW}3. MyPy - Type checking${NC}"
if mypy src/ --strict --ignore-missing-imports; then
    echo -e "${GREEN}✓ MyPy type checking passed${NC}\n"
else
    echo -e "${RED}✗ MyPy found type errors (see above)${NC}\n"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Summary
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}✓ All code quality checks passed!${NC}"
else
    echo -e "${RED}✗ $FAIL_COUNT check(s) failed${NC}"
    exit 1
fi
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}\n"
