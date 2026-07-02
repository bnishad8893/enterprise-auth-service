# Database Design

Database schema, relationships, and design decisions.

## Design Principles

- Normalize data to 3NF (Third Normal Form)
- Use surrogate keys (UUID) for all tables
- Use appropriate data types and constraints
- Implement referential integrity
- Index for query performance

## Core Tables

### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(254) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_login TIMESTAMP,
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_active ON users(is_active);
```

### User Profiles Table

```sql
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    avatar_url TEXT,
    phone VARCHAR(20),
    timezone VARCHAR(50) DEFAULT 'UTC',
    enabled_2fa BOOLEAN DEFAULT FALSE,
    preferences JSONB DEFAULT '{}',
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
```

### Authentication Tokens Table

```sql
CREATE TABLE auth_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    token_type VARCHAR(20) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    issued_at TIMESTAMP NOT NULL DEFAULT NOW(),
    revoked BOOLEAN DEFAULT FALSE,
    revoked_at TIMESTAMP,
    CONSTRAINT valid_token_type CHECK (token_type IN ('access', 'refresh'))
);

CREATE INDEX idx_auth_tokens_user_id ON auth_tokens(user_id);
CREATE INDEX idx_auth_tokens_token_hash ON auth_tokens(token_hash);
CREATE INDEX idx_auth_tokens_expires_at ON auth_tokens(expires_at);
CREATE INDEX idx_auth_tokens_revoked ON auth_tokens(revoked);
```

### Audit Logs Table

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50),
    resource_id UUID,
    ip_address INET,
    user_agent TEXT,
    status VARCHAR(20) NOT NULL,
    details JSONB DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT valid_status CHECK (status IN ('success', 'failure', 'warning'))
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
```

### Roles Table

```sql
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_roles_name ON roles(name);
```

### Permissions Table

```sql
CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codename VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    resource_type VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_permissions_codename ON permissions(codename);
```

### Role Permissions Junction Table

```sql
CREATE TABLE role_permissions (
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

CREATE INDEX idx_role_permissions_role ON role_permissions(role_id);
CREATE INDEX idx_role_permissions_permission ON role_permissions(permission_id);
```

### User Roles Junction Table

```sql
CREATE TABLE user_roles (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, role_id)
);

CREATE INDEX idx_user_roles_user ON user_roles(user_id);
CREATE INDEX idx_user_roles_role ON user_roles(role_id);
```

## Entity Relationships

```
users (1) ──── (1) user_profiles
  │
  ├─── (1) ──── (N) auth_tokens
  │
  ├─── (1) ──── (N) audit_logs
  │
  └─── (N) ──── (N) roles
         │
         └─── (N) ──── (N) permissions
```

## Indexing Strategy

### Query Performance Indices

- `users.email`: Fast user lookup by email
- `auth_tokens.token_hash`: Token validation
- `audit_logs.created_at`: Time-range queries
- `audit_logs.user_id`: User activity retrieval

### Maintenance Indices

- Regular VACUUM ANALYZE to update statistics
- Monitor slow queries and add indices as needed
- Avoid over-indexing (increases write overhead)

## Constraints

### Data Integrity

- Email format validation
- Unique email per user
- Required fields: email, password_hash
- Referential integrity for all foreign keys
- Token type enumeration

### Business Logic Constraints

- User cannot have duplicate roles
- Token must have valid type
- Soft deletes via is_active flag
- Audit log immutability

## Performance Optimization

### Query Performance

- Use connection pooling (PgBouncer)
- N+1 query prevention (ORM select_related)
- Batch operations when possible
- Regular query analysis and optimization

### Table Maintenance

```sql
-- Analyze query performance
ANALYZE users;

-- Reindex table
REINDEX TABLE users;

-- Vacuum deadspace
VACUUM FULL ANALYZE users;
```

### Partitioning Strategy

For high-volume tables (future):

```sql
-- Partition audit_logs by month
CREATE TABLE audit_logs_2024_01 PARTITION OF audit_logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

## Backup and Recovery

### Backup Strategy

- Daily full backups
- Point-in-time recovery enabled
- Physical backups using pg_basebackup
- Test restores regularly

### Recovery Procedures

```bash
# Point-in-time recovery
pg_basebackup -h localhost -D /path/to/backup -P -v -X stream

# Restore to specific time
RECOVERY_TARGET_TIMELINE = 'latest'
RECOVERY_TARGET_TIME = '2024-01-15 12:00:00'
```

## Migration Strategy

### Safe Schema Changes

1. Plan migration thoroughly
2. Test on staging environment
3. Create backup before applying
4. Run migration during maintenance window
5. Verify data integrity
6. Monitor application after change

### Avoiding Downtime

- Add column as nullable, populate, then add NOT NULL
- Create new indices before dropping old ones
- Use feature flags for gradual rollout
- Maintain backward compatibility

## Monitoring

### Health Checks

```sql
-- Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Check slow queries
SELECT query, calls, mean_time, max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

### Performance Tuning

- Monitor cache hit ratio
- Adjust shared_buffers based on available RAM
- Configure effective_cache_size
- Tune work_mem for complex queries

