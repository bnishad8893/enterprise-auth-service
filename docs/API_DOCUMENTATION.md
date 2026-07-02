# API Documentation

Complete REST API reference and specifications.

## Overview

The Authentication Service provides REST endpoints for user management and authentication operations.

All endpoints return JSON responses with appropriate HTTP status codes.

## Base URL

- Development: `http://localhost:8000/api/v1`
- Production: `https://api.example.com/api/v1`

## Authentication

Requests are authenticated using JWT Bearer tokens in the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

## Response Format

All responses follow a consistent format:

### Success Response

```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Operation successful"
}
```

### Error Response

```json
{
  "success": false,
  "errors": [
    {
      "field": "email",
      "message": "Email already exists"
    }
  ],
  "message": "Validation failed"
}
```

## Endpoints

### Authentication

#### POST /auth/register
Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### POST /auth/login
Authenticate user and receive JWT tokens.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "access_token": "jwt_token",
    "refresh_token": "refresh_token",
    "user": { /* user object */ }
  }
}
```

#### POST /auth/logout
Invalidate authentication tokens.

**Response:** `200 OK`

#### POST /auth/refresh
Generate new access token using refresh token.

**Request:**
```json
{
  "refresh_token": "refresh_token"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "access_token": "new_jwt_token"
  }
}
```

### Users

#### GET /users/me
Get current authenticated user profile.

**Response:** `200 OK`

#### PUT /users/me
Update current user profile.

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:** `200 OK`

#### POST /users/change-password
Change current user password.

**Request:**
```json
{
  "current_password": "OldPassword123!",
  "new_password": "NewPassword123!"
}
```

**Response:** `200 OK`

## Status Codes

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `500 Internal Server Error`: Server error

## Rate Limiting

API endpoints are rate-limited to prevent abuse:

- 1000 requests per hour per user
- 10000 requests per hour per IP

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1234567890
```

## Error Handling

Detailed error responses include field-level validation errors and specific error codes for programmatic handling.

## Pagination

List endpoints support pagination:

```
GET /users?page=1&page_size=20
```

Response includes pagination metadata:

```json
{
  "count": 100,
  "next": "http://api.example.com/users?page=2",
  "previous": null,
  "results": [ /* items */ ]
}
```

## Filtering and Sorting

List endpoints support filtering and sorting via query parameters.

See individual endpoint documentation for supported filters.

## Testing

Use the included Postman collection to test API endpoints:

1. Import `postman/auth-service.postman_collection.json`
2. Set environment variables in `postman/environment.postman_environment.json`
3. Run requests or collection via Postman or Newman CLI

## Versioning

API follows semantic versioning. Current version is v1.

Future versions will be accessible via `/api/v2`, etc.

Deprecated endpoints will include deprecation notices and migration guidance.

