#!/bin/bash
# setup.sh - Initialize development environment
# Usage: ./scripts/setup.sh
# This script sets up uv, creates virtual environment, installs dependencies, and configures pre-commit

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Enterprise Auth Service - Development Environment Setup${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to print error
print_error() {
    echo -e "${RED}✗${NC} $1"
    exit 1
}

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
echo -e "\n${YELLOW}Python version:${NC} $PYTHON_VERSION"
if [[ "$PYTHON_VERSION" != "3.13" ]]; then
    print_error "Python 3.13 is required. Found: $PYTHON_VERSION"
fi
print_status "Python 3.13 detected"

# Install/upgrade uv
echo -e "\n${YELLOW}Step 1: Installing uv package manager...${NC}"
pip install --upgrade uv || print_error "Failed to install uv"
print_status "uv installed"

# Create virtual environment
echo -e "\n${YELLOW}Step 2: Creating virtual environment...${NC}"
if [ -d ".venv" ]; then
    print_status "Virtual environment already exists"
else
    uv venv .venv || print_error "Failed to create virtual environment"
    print_status "Virtual environment created"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Step 3: Activating virtual environment...${NC}"
source .venv/bin/activate
print_status "Virtual environment activated"

# Install dependencies
echo -e "\n${YELLOW}Step 4: Installing dependencies...${NC}"
uv pip install --upgrade pip setuptools wheel || print_error "Failed to upgrade pip"
print_status "Upgraded pip, setuptools, wheel"

uv pip install -e ".[dev,test]" || print_error "Failed to install project dependencies"
print_status "Project dependencies installed"

# Create .env file if it doesn't exist
echo -e "\n${YELLOW}Step 5: Setting up environment configuration...${NC}"
if [ -f ".env" ]; then
    print_status ".env file already exists"
else
    cp .env.example .env
    print_status "Created .env from .env.example - Update with your settings"
fi

# Setup pre-commit hooks
echo -e "\n${YELLOW}Step 6: Setting up pre-commit hooks...${NC}"
if [ ! -d ".git" ]; then
    print_status "Not a git repository, skipping pre-commit setup"
else
    pre-commit install || print_error "Failed to install pre-commit hooks"
    print_status "Pre-commit hooks configured"
fi

# Create necessary directories
echo -e "\n${YELLOW}Step 7: Creating application directories...${NC}"
mkdir -p logs media static
print_status "Application directories created"

echo -e "\n${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Development environment setup complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. Activate the virtual environment: source .venv/bin/activate"
echo "2. Update .env with your configuration"
echo "3. Run tests: ./scripts/test.sh"
echo "4. Start development: ./scripts/run.sh"
echo ""
