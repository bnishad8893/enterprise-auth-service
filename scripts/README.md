# Scripts

This directory contains utility scripts for development and operations.

## Script Categories

- **database/**: Database initialization and migrations
- **dev/**: Development environment setup scripts
- **deploy/**: Deployment and rollout scripts
- **maintenance/**: Operational maintenance tasks
- **backup/**: Backup and restore procedures
- **monitoring/**: Health checks and diagnostics

## Guidelines

- All scripts should be idempotent where possible
- Include error handling and validation
- Document parameters and usage
- Support dry-run modes for destructive operations
- Include logging for audit trails

## Execution

Scripts should be executed from the project root using: `./scripts/<script_name>.sh`
