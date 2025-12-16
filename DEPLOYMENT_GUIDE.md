# Deployment Guide for CRM System

## Pre-Deployment Checklist

### 1. Google Cloud Project Setup
Ensure you have access to the `danielsbonnin-com` Google Cloud project with the following:
- ✅ Cloud SQL instance created and running
- ✅ Firestore database enabled
- ✅ Cloud Run service configured
- ✅ IAM permissions for deployment

### 2. Database Configuration

#### Create Cloud SQL Database
```sql
-- Connect to your Cloud SQL PostgreSQL instance
CREATE DATABASE crocheted_crumb;

-- Grant permissions to your application user
GRANT ALL PRIVILEGES ON DATABASE crocheted_crumb TO your_app_user;
```

#### Configure Connection
The application will automatically initialize the schema on first run. You can also manually run:
```bash
python -c "from database import init_db_pool, init_database_schema; init_db_pool(); init_database_schema()"
```

### 3. Environment Variables for Cloud Run

Set these environment variables in Cloud Run:

```bash
# Database Configuration
DB_HOST=/cloudsql/danielsbonnin-com:us-central1:YOUR_INSTANCE_NAME
DB_NAME=crocheted_crumb
DB_USER=your-database-user
DB_PASSWORD=your-secure-database-password
DB_PORT=5432

# Firestore Configuration
GOOGLE_CLOUD_PROJECT=danielsbonnin-com
FIRESTORE_COLLECTION_PREFIX=sarah_site_

# Stripe Configuration (use test keys initially)
STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Admin Configuration
ADMIN_USERNAME=admin
ADMIN_PASSWORD=CHANGE_THIS_TO_SECURE_PASSWORD

# Flask Configuration
SECRET_KEY=GENERATE_A_RANDOM_SECRET_KEY_HERE
FLASK_ENV=production
PORT=8080
```

**Important Security Notes:**
- Generate a strong random SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`
- Use a strong ADMIN_PASSWORD (min 16 characters, mixed case, numbers, symbols)
- Never commit these values to the repository

### 4. Update Cloud Build Configuration

The `cloudbuild.yaml` is already configured. Just ensure environment variables are set in Cloud Run.

You may need to add Cloud SQL connection to the Cloud Run service:
```bash
gcloud run services update sarah-danielsbonnin-com \
  --add-cloudsql-instances danielsbonnin-com:us-central1:YOUR_INSTANCE_NAME \
  --region us-central1
```

## Deployment Steps

### Option 1: Automatic Deployment (Recommended)
1. Push to main branch:
   ```bash
   git push origin main
   ```
2. Cloud Build will automatically:
   - Build the Docker container
   - Push to Artifact Registry
   - Deploy to Cloud Run
3. Monitor deployment in Cloud Console

### Option 2: Manual Deployment
```bash
# Build the container
gcloud builds submit --config cloudbuild.yaml

# Or build and deploy manually
docker build -t us-central1-docker.pkg.dev/danielsbonnin-com/danielsbonnin-com/sarah-danielsbonnin-com:latest .
docker push us-central1-docker.pkg.dev/danielsbonnin-com/danielsbonnin-com/sarah-danielsbonnin-com:latest

gcloud run deploy sarah-danielsbonnin-com \
  --image us-central1-docker.pkg.dev/danielsbonnin-com/danielsbonnin-com/sarah-danielsbonnin-com:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

## Post-Deployment Steps

### 1. Verify Database Connection
Check Cloud Run logs to ensure database connection is successful:
```bash
gcloud run logs read sarah-danielsbonnin-com --region us-central1 --limit 50
```

Look for:
- ✓ Database connection pool created successfully
- ✓ Database schema initialized successfully

### 2. Load Sample Data
SSH into Cloud Run or use Cloud Shell:
```bash
# Connect to your Cloud SQL instance via proxy
cloud_sql_proxy -instances=danielsbonnin-com:us-central1:YOUR_INSTANCE=tcp:5432

# In another terminal, set env vars and run sample data script
export DB_HOST=localhost
export DB_NAME=crocheted_crumb
export DB_USER=your-user
export DB_PASSWORD=your-password
python generate_sample_data.py
```

Or create a one-time Cloud Run job:
```bash
gcloud run jobs create load-sample-data \
  --image us-central1-docker.pkg.dev/danielsbonnin-com/danielsbonnin-com/sarah-danielsbonnin-com:latest \
  --region us-central1 \
  --set-env-vars DB_HOST=/cloudsql/danielsbonnin-com:us-central1:YOUR_INSTANCE,DB_NAME=crocheted_crumb \
  --set-secrets DB_PASSWORD=DB_PASSWORD:latest,DB_USER=DB_USER:latest \
  --command python \
  --args generate_sample_data.py

gcloud run jobs execute load-sample-data --region us-central1
```

### 3. Test Admin Access
1. Visit: https://sarah.danielsbonnin.com/admin/login
2. Log in with credentials from environment variables
3. Verify dashboard loads with sample data
4. Test each admin section (customers, products, orders, inquiries)

### 4. Test Public Features
1. Visit: https://sarah.danielsbonnin.com/products
2. Browse products by category
3. Add items to cart
4. Complete checkout process (stub payment)
5. Verify order appears in admin

### 5. Test Contact Form
1. Visit: https://sarah.danielsbonnin.com/contact
2. Submit an inquiry
3. Verify it appears in admin inquiries section
4. Check Firestore for analytics entry

## Monitoring & Maintenance

### Check Application Health
```bash
# View recent logs
gcloud run logs read sarah-danielsbonnin-com --region us-central1 --limit 100

# Monitor metrics
gcloud run services describe sarah-danielsbonnin-com --region us-central1
```

### Database Maintenance
```bash
# Connect to Cloud SQL
gcloud sql connect YOUR_INSTANCE --user=postgres --database=crocheted_crumb

# Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

# Vacuum and analyze
VACUUM ANALYZE;
```

### Backup Strategy
1. **Automated Backups**: Enable Cloud SQL automated backups
   ```bash
   gcloud sql instances patch YOUR_INSTANCE \
     --backup-start-time=02:00 \
     --enable-bin-log
   ```

2. **Manual Backup**:
   ```bash
   gcloud sql backups create --instance=YOUR_INSTANCE
   ```

3. **Export Data**:
   ```bash
   gcloud sql export sql YOUR_INSTANCE gs://your-backup-bucket/backup-$(date +%Y%m%d).sql \
     --database=crocheted_crumb
   ```

## Troubleshooting

### Issue: Database Connection Failed
**Symptoms**: Logs show "Error creating connection pool"

**Solutions**:
1. Verify Cloud SQL instance is running
2. Check Cloud Run has Cloud SQL connection configured
3. Verify environment variables are set correctly
4. Ensure database user has correct permissions

### Issue: Admin Login Not Working
**Symptoms**: "Invalid credentials" message

**Solutions**:
1. Verify ADMIN_USERNAME and ADMIN_PASSWORD environment variables
2. Check SECRET_KEY is set for session management
3. Clear browser cookies
4. Check Cloud Run logs for errors

### Issue: Products Not Showing
**Symptoms**: Empty product catalog

**Solutions**:
1. Check if sample data was loaded
2. Verify database connection is working
3. Check Cloud Run logs for query errors
4. Manually add a product via admin interface

### Issue: Contact Form Not Saving
**Symptoms**: Form submits but no inquiry in database

**Solutions**:
1. Check database connection
2. Verify inquiries table exists
3. Check for validation errors in logs
4. Test database insert permissions

## Rollback Procedure

If deployment causes issues:

```bash
# List recent revisions
gcloud run revisions list --service sarah-danielsbonnin-com --region us-central1

# Rollback to previous revision
gcloud run services update-traffic sarah-danielsbonnin-com \
  --to-revisions PREVIOUS_REVISION=100 \
  --region us-central1
```

## Scaling Configuration

Adjust Cloud Run settings for traffic:

```bash
gcloud run services update sarah-danielsbonnin-com \
  --region us-central1 \
  --min-instances 0 \
  --max-instances 10 \
  --concurrency 80 \
  --cpu 1 \
  --memory 512Mi
```

## Cost Optimization

1. **Database**: Use smallest instance size needed
2. **Cloud Run**: Set min-instances to 0 for low traffic
3. **Cloud Storage**: Enable object lifecycle policies for backups
4. **Monitoring**: Set up budget alerts

## Security Hardening

1. **Rotate Secrets Regularly**: Update admin password, secret keys
2. **Enable Audit Logging**: Track all admin actions
3. **Set Up Alerts**: Monitor for unusual activity
4. **Regular Updates**: Keep dependencies updated
5. **Database Security**: Use SSL connections, restrict IP access

## Success Criteria

✅ Cloud Run service is healthy
✅ Database connection is established
✅ Sample data is loaded (or real products added)
✅ Admin panel is accessible
✅ Public product catalog works
✅ Cart and checkout flow complete
✅ Contact form saves to database
✅ No errors in Cloud Run logs
✅ HTTPS certificate is valid
✅ Monitoring alerts are configured

## Support Contacts

- **Technical Issues**: Check Cloud Console logs
- **Database Issues**: Cloud SQL documentation
- **Deployment Issues**: Cloud Run documentation
- **General Questions**: snbonnin@gmail.com
