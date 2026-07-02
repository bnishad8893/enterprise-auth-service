# Security Architecture

Comprehensive security design and threat mitigation strategies.

## Security Principles

- Principle of Least Privilege (PoLP)
- Defense in Depth
- Secure by Default
- Fail Securely
- Never Trust User Input
- Separation of Concerns

## Authentication Security

### Password Storage

- **Algorithm**: Argon2id (industry standard)
- **Parameters**:
  - Time cost (iterations): 2
  - Memory cost: 65536 KB
  - Parallelism: 4 threads
- All passwords hashed server-side
- Never log or transmit passwords in plain text

```python
from argon2 import PasswordHasher

hasher = PasswordHasher()
hashed_password = hasher.hash(password)
hasher.verify(hashed_password, password)
```

### JWT Token Security

#### Access Token

- **Type**: JWT (JSON Web Token)
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Expiration**: 15 minutes (short-lived)
- **Claims**: user_id, email, roles, permissions
- **Signing**: Server-side secret key
- **Storage**: Memory (not localStorage if possible)

#### Refresh Token

- **Type**: Opaque token (random string)
- **Expiration**: 7 days
- **Storage**: Secure HTTP-only cookie or secure storage
- **Invalidation**: Revoked on logout
- **Rotation**: New refresh token on each use

#### Token Revocation

Tokens are revoked by:

1. Adding token to Redis blacklist with TTL
2. Storing revoked token hash in database
3. Checking revocation status on validation

```python
# Token revocation implementation
redis.setex(f"revoked_token:{token_hash}", token_ttl, "1")
```

### Session Management

- HTTP-only cookies for session tokens
- Secure flag for HTTPS only
- SameSite=Strict to prevent CSRF
- Automatic session timeout (30 minutes)
- Session fixation prevented through token regeneration

## Authorization Security

### Role-Based Access Control (RBAC)

```
User → Role(s) → Permission(s) → Resource Access
```

#### Default Roles

1. **User**: Regular user permissions
2. **Admin**: Full system access
3. **ServiceAccount**: Machine-to-machine access
4. **Guest**: Limited public access

#### Permission Model

- Resource-based: Check resource ownership
- Action-based: Read, Write, Delete, Admin
- Time-based: Permissions valid for time periods
- Conditional: Based on context (IP, time, etc.)

### Access Control Enforcement

All endpoints enforce:

1. Authentication: User identity verified
2. Authorization: User has required permissions
3. Resource ownership: User owns the resource
4. Rate limiting: Request quota respected

## Network Security

### HTTPS/TLS

- **Minimum**: TLS 1.3
- **Certificate**: Signed by trusted CA
- **Renewal**: Automated (Let's Encrypt or similar)
- **HSTS**: Strict-Transport-Security header
- **Certificate Pinning**: For critical APIs

### CORS (Cross-Origin Resource Sharing)

```python
# Only allow specific origins
CORS_ALLOWED_ORIGINS = [
    "https://app.example.com",
    "https://admin.example.com",
]

# Disallow credentials by default
CORS_ALLOW_CREDENTIALS = False
```

### API Rate Limiting

Per-endpoint rate limits:

```
- Public endpoints: 100 requests/minute
- Authenticated endpoints: 1000 requests/minute
- Admin endpoints: 10000 requests/minute
```

Implemented using Redis:

```python
# Rate limit implementation
def check_rate_limit(user_id, endpoint, limit=1000):
    key = f"rate_limit:{user_id}:{endpoint}"
    current = redis.incr(key)
    if current == 1:
        redis.expire(key, 60)
    return current <= limit
```

## Input Validation and Output Encoding

### Input Validation

- **Type checking**: Correct data types expected
- **Length validation**: Appropriate string lengths
- **Format validation**: Email, URL, phone formats
- **Range validation**: Numbers within acceptable range
- **Whitelist validation**: Only allowed values accepted

Example:

```python
class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(
        min_length=12,
        max_length=128,
        validators=[
            MinimumPasswordStrengthValidator()
        ]
    )
    first_name = serializers.CharField(max_length=100)
```

### Output Encoding

- **JSON**: Properly escaped for JSON context
- **HTML**: HTML entities escaped if rendering HTML
- **URL**: URL encoded if in URL
- **CSV**: Proper CSV escaping if exporting

## Data Security

### Sensitive Data Protection

#### Data Classification

- **Public**: Can be cached and logged
- **Internal**: Restricted access, limited logging
- **Confidential**: Encrypted, minimal logging
- **Secret**: Highly restricted, encrypted at rest and transit

#### Sensitive Fields

- Passwords: Never logged, encrypted, hash only
- Tokens: Not logged, encrypted in storage
- API Keys: Not displayed in logs
- Personal data: Minimized in logs

#### Encryption

```python
# At-rest encryption for sensitive fields
class User(models.Model):
    email = models.EmailField()
    # Encrypt sensitive fields
    ssn = EncryptedTextField()
```

### Data Minimization

- Collect only necessary data
- Retain data only as long as needed
- Purge old data automatically
- Offer data export and deletion

## Threat Models

### Common Threats and Mitigation

#### SQL Injection

**Threat**: Malicious SQL in input

**Mitigation**:
- Use ORM (Django ORM prevents SQL injection)
- Parameterized queries
- Input validation and sanitization
- Least privilege database accounts

#### Cross-Site Scripting (XSS)

**Threat**: JavaScript injected in user input

**Mitigation**:
- Output encoding
- Content Security Policy (CSP) headers
- HTTPOnly cookies
- Input validation

#### Cross-Site Request Forgery (CSRF)

**Threat**: Unauthorized actions from other sites

**Mitigation**:
- CSRF tokens in forms
- SameSite cookies
- Origin/Referer header validation
- State-changing operations require POST

#### Brute Force Attacks

**Threat**: Multiple failed login attempts

**Mitigation**:
- Rate limiting on login endpoint
- Account lockout after N attempts
- Progressive delays between attempts
- Require CAPTCHA after failures

#### DDoS Attacks

**Threat**: Service disruption through volume

**Mitigation**:
- Rate limiting
- DDoS protection service (CloudFlare, AWS Shield)
- Load balancing
- Auto-scaling

#### Man-in-the-Middle (MITM)

**Threat**: Intercepting communications

**Mitigation**:
- TLS/SSL enforcement
- Certificate pinning
- Secure headers (HSTS)
- No unencrypted communication

## Security Monitoring

### Logging Security Events

```python
# Log security-relevant events
logger = logging.getLogger('security')

logger.warning(f"Failed login attempt: {email} from {ip_address}")
logger.info(f"User password changed: {user_id}")
logger.error(f"Rate limit exceeded: {user_id} on {endpoint}")
```

### Security Alerts

Monitor for:

- Multiple failed login attempts
- Unusual access patterns
- Rate limit violations
- Token revocation patterns
- Permission escalation attempts
- Data access anomalies

### Audit Trail

All security-sensitive operations logged:

- Authentication events
- Authorization changes
- Permission modifications
- Data access and modifications
- Configuration changes
- System events

```sql
SELECT created_at, user_id, action, resource_type, status, details
FROM audit_logs
WHERE action IN ('login', 'logout', 'password_change')
ORDER BY created_at DESC;
```

## Security Best Practices

### Development

- [ ] Use authenticated Git commits (GPG signing)
- [ ] Enable branch protection
- [ ] Require code review before merge
- [ ] Use security-focused linting (Bandit)
- [ ] Dependency vulnerability scanning (Safety)
- [ ] SAST (Static Application Security Testing)

### Deployment

- [ ] Secrets in environment variables or secrets manager
- [ ] Immutable infrastructure
- [ ] Minimal container images
- [ ] Security scanning of images
- [ ] Network segmentation
- [ ] Least privilege IAM roles

### Operations

- [ ] Regular security updates
- [ ] Patch management process
- [ ] Intrusion detection
- [ ] Log aggregation and monitoring
- [ ] Incident response plan
- [ ] Regular security audits

### Incident Response

1. **Detection**: Alert triggered
2. **Analysis**: Understand scope and impact
3. **Containment**: Prevent further damage
4. **Eradication**: Remove threat
5. **Recovery**: Restore normal operations
6. **Lessons Learned**: Document and improve

## Compliance Considerations

### GDPR

- Data subject rights (access, deletion)
- Consent management
- Data breach notification
- Privacy by design

### CCPA

- Consumer privacy rights
- Opt-out mechanisms
- Data disclosure

### SOC 2

- Access controls
- Monitoring and logging
- Change management
- Incident response

