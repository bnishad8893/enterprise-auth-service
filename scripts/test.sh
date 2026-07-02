#!/bin/bash
# test.sh - Run pytest with coverage reporting
# Usage: ./scripts/test.sh [unit|integration|all|--cov|--verbose]

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    source .venv/bin/activate
fi

echo -e "${YELLOW}Running tests with pytest...${NC}\n"

# Default pytest arguments
PYTEST_ARGS=("--strict-markers" "--tb=short")

# Parse arguments
for arg in "$@"; do
    case $arg in
        unit)
            PYTEST_ARGS+=("-m" "unit")
            ;;
        integration)
            PYTEST_ARGS+=("-m" "integration")
            ;;
        --cov)
            PYTEST_ARGS+=("--cov=src" "--cov-report=html" "--cov-report=term-missing")
            ;;
        --verbose)
            PYTEST_ARGS+=("-vv")
            ;;
        --fast)
            PYTEST_ARGS+=("-m" "not slow")
            ;;
        *)
            PYTEST_ARGS+=("$arg")
            ;;
    esac
done

# Add default coverage if no specific marker given
if [[ ! " ${PYTEST_ARGS[@]} " =~ " -m " ]]; then
    PYTEST_ARGS+=("--cov=src" "--cov-report=term-missing" "--cov-report=html")
fi

echo -e "${YELLOW}pytest arguments:${NC} ${PYTEST_ARGS[@]}\n"

# Run tests
pytest "${PYTEST_ARGS[@])" tests/

echo -e "\n${GREEN}✓ Tests complete${NC}"
echo -e "${YELLOW}Coverage HTML report: htmlcov/index.html${NC}\n"
