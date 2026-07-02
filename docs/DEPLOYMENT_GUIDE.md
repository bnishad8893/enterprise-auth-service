# Deployment Guide

Instructions for deploying the application to production environments.

## Deployment Strategies

### Docker Compose (Staging/Development)

Suitable for smaller deployments or testing production-like environments.

1. Prepare environment
```bash
cp .env.example .env.prod
# Edit .env.prod with production values
```

2. Deploy with Compose
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. Run migrations
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### Kubernetes (Production)

Recommended for enterprise deployments with horizontal scaling and high availability.

#### Prerequisites

- Kubernetes cluster (EKS, GKE, AKS, or self-managed)
- kubectl configured
- Docker images pushed to registry
- Secrets configured in cluster

#### Deployment Steps

1. Configure secrets
```bash
kubectl create secret generic app-secrets \
  --from-literal=SECRET_KEY=your-secret-key \
  --from-literal=DATABASE_URL=postgresql://... \
  --from-literal=REDIS_URL=redis://...
```

2. Create namespace
```bash
kubectl create namespace production
```

3. Deploy application
```bash
kubectl apply -f deployment/kubernetes/ -n production
```

4. Run migrations
```bash
kubectl exec -it -n production deployment/app -- \
  python manage.py migrate
```

5. Verify deployment
```bash
kubectl get pods -n production
kubectl logs -n production -l app=auth-service
```

#### Health Checks

Application exposes health endpoints:

- `/health/ready`: Readiness probe
- `/health/live`: Liveness probe

Kubernetes configuration:

```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 60
  periodSeconds: 30
```

## Cloud Platform Deployments

### AWS ECS

Provides managed container orchestration without full Kubernetes complexity.

Configuration in `deployment/aws/ecs/`:

```bash
# Deploy cluster
terraform apply -var-file=production.tfvars

# Update service
aws ecs update-service --cluster production --service api --force-new-deployment
```

### AWS Lambda

For serverless deployment:

```bash
# Package application
zip -r lambda-package.zip src/ requirements.txt

# Deploy function
aws lambda update-function-code \
  --function-name auth-service \
  --zip-file fileb://lambda-package.zip
```

### Google Cloud Run

Containerized servless option:

```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/auth-service

# Deploy
gcloud run deploy auth-service \
  --image gcr.io/PROJECT_ID/auth-service \
  --region us-central1 \
  --platform managed
```

## Pre-Deployment Checklist

- [ ] All tests passing locally
- [ ] Code review approved
- [ ] Security scan passed
- [ ] Secrets configured securely
- [ ] Database backups taken
- [ ] Rollback plan documented
- [ ] Monitoring alerts configured
- [ ] Load testing completed

## Database Migrations

### Safe Migration Process

1. Create migration
```bash
python manage.py makemigrations
```

2. Test locally
```bash
python manage.py migrate
pytest  # Run full test suite
```

3. Review migration code
```bash
git diff src/migrations/
```

4. Deploy migrations
```bash
# Backup database first
pg_dump -h host -U user database > backup.sql

# Run migrations
python manage.py migrate
```

### Rollback Procedure

If migration fails:

```bash
# List migrations
python manage.py showmigrations

# Revert to previous
python manage.py migrate app_name PREVIOUS_MIGRATION_NAME

# Restore from backup
psql -h host -U user database < backup.sql
```

## Scaling

### Horizontal Scaling

Kubernetes automatically scales replicas:

```yaml
autoscaling:
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

### Database Scaling

For large datasets:

- Use read replicas for read-heavy operations
- Implement connection pooling (PgBouncer)
- Shard data if necessary
- Archive old data

### Cache Scaling

Redis cluster configuration in `deployment/redis/`:

```bash
redis-cli cluster create host1:7000 host2:7000 host3:7000 \
  host4:7001 host5:7001 host6:7001
```

## Monitoring and Logging

### Application Logs

Logs are aggregated to:

- CloudWatch (AWS)
- Cloud Logging (GCP)
- Stack Driver (Azure)

### Metrics

Key metrics to monitor:

- Request latency (p50, p95, p99)
- Error rate
- Database connection pool usage
- Redis hit rate
- CPU and memory usage
- Disk I/O

### Alerting

Configure alerts for:

- Error rate > 1%
- Response time > 2s
- Database connection pool exhaustion
- Redis memory usage > 80%
- Disk usage > 85%

## Backup and Recovery

### Database Backup

Daily automated backups:

```bash
# Manual backup
pg_dump -h $DB_HOST -U $DB_USER $DB_NAME | gzip > backup_$(date +%Y%m%d).sql.gz

# Restore
gunzip < backup_20240101.sql.gz | psql -h $DB_HOST -U $DB_USER $DB_NAME
```

### Data Recovery

For data loss:

1. Identify issue
2. Stop write operations
3. Restore from backup
4. Verify data integrity
5. Document incident

## Security Hardening

### TLS/SSL

- All traffic encrypted in transit
- Certificate management via Let's Encrypt or ACM
- Auto-renewal configured

### Secrets Management

- Use AWS Secrets Manager, GCP Secret Manager, or HashiCorp Vault
- Never commit secrets
- Rotate secrets regularly
- Audit secret access

### Network Security

- Use VPC/Virtual Networks
- Restrict ingress to required ports
- Use security groups appropriately
- Enable WAF (Web Application Firewall)

## Performance Optimization

### Caching Strategy

- Cache API responses
- Cache database query results
- Set appropriate TTL values
- Monitor cache hit rates

### Database Optimization

- Add missing indexes
- Analyze slow queries
- Optimize N+1 queries
- Use materialized views for complex queries

### Application Optimization

- Profile and identify bottlenecks
- Use async tasks for long operations
- Implement pagination
- Compress responses (gzip)

## Disaster Recovery

### RTO and RPO

- **RTO** (Recovery Time Objective): < 1 hour
- **RPO** (Recovery Point Objective): < 15 minutes

### Failover Procedure

1. Detect failure (automated alerts)
2. Promote read replica or start standby
3. Update DNS/load balancer
4. Verify service health
5. Notify stakeholders

### Testing

- Conduct monthly disaster recovery drills
- Document all procedures
- Keep runbooks updated

## Rollback Procedures

### Application Rollback

```bash
# Revert to previous deployment
kubectl rollout undo deployment/app -n production

# Check rollout status
kubectl rollout status deployment/app -n production
```

### Database Rollback

Use backup from before migration:

```bash
psql -h host -U user database < backup_pre_migration.sql
```

## Post-Deployment

- [ ] Verify all services are running
- [ ] Check application logs for errors
- [ ] Test critical user flows
- [ ] Monitor metrics and alerts
- [ ] Notify stakeholders of successful deployment
- [ ] Update documentation

