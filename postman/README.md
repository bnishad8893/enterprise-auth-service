# Postman Collections

This directory contains Postman API collections for testing and documentation.

## Collections

- **auth-service.postman_collection.json**: Complete API endpoint collection
- **environment.postman_environment.json**: Environment variables for different deployments
- **globals.postman_globals.json**: Global variables shared across collections

## Usage

1. Import collections into Postman
2. Set appropriate environment variables
3. Run requests individually or as an automated collection run
4. Use Collection Runner for regression testing

## CI/CD Integration

Collections can be run via Postman CLI:
```bash
newman run auth-service.postman_collection.json -e environment.postman_environment.json
```

## Maintenance

- Update collections when API changes
- Version collections alongside code releases
- Keep test scenarios current with features
