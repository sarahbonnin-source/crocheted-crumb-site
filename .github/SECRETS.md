# GitHub Secrets Configuration

This document describes the GitHub secrets required for the deployment workflows.

## Required Secrets

The following secrets need to be configured in your GitHub repository settings:

### 1. `WIF_PROVIDER`
**Description:** Workload Identity Federation Provider resource name for Google Cloud

**Format:** 
```
projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_NAME/providers/PROVIDER_NAME
```

**How to get it:**
1. Go to Google Cloud Console → IAM & Admin → Workload Identity Federation
2. Find your pool and provider
3. Copy the full resource name

### 2. `WIF_SERVICE_ACCOUNT`
**Description:** Google Cloud Service Account email for Workload Identity Federation

**Format:**
```
SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com
```

**How to get it:**
1. Go to Google Cloud Console → IAM & Admin → Service Accounts
2. Find or create a service account with the following roles:
   - `Cloud Run Admin`
   - `Artifact Registry Writer`
   - `Service Account User`
3. Copy the email address

### 3. `GCP_PROJECT_ID`
**Description:** Your Google Cloud Project ID

**Format:**
```
your-project-id
```

**How to get it:**
1. Go to Google Cloud Console
2. Your Project ID is shown at the top of the page

## Setting Up Workload Identity Federation

If you haven't set up Workload Identity Federation yet, follow these steps:

### 1. Create a Workload Identity Pool

```bash
gcloud iam workload-identity-pools create "github-pool" \
  --project="YOUR_PROJECT_ID" \
  --location="global" \
  --display-name="GitHub Actions Pool"
```

### 2. Create a Workload Identity Provider

```bash
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="YOUR_PROJECT_ID" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --display-name="GitHub Actions Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

### 3. Create or Configure Service Account

```bash
# Create service account
gcloud iam service-accounts create github-actions-deploy \
  --display-name="GitHub Actions Deploy"

# Grant necessary roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-actions-deploy@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-actions-deploy@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-actions-deploy@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```

### 4. Allow GitHub Actions to Impersonate Service Account

```bash
gcloud iam service-accounts add-iam-policy-binding github-actions-deploy@YOUR_PROJECT_ID.iam.gserviceaccount.com \
  --project="YOUR_PROJECT_ID" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME"
```

### 5. Get the WIF_PROVIDER value

```bash
gcloud iam workload-identity-pools providers describe "github-provider" \
  --project="YOUR_PROJECT_ID" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --format="value(name)"
```

## Adding Secrets to GitHub

1. Go to your GitHub repository
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with its name and value

## Testing the Setup

After configuring the secrets:

1. Create a test branch and open a Pull Request
2. Check the **Actions** tab to see if the preview deployment runs successfully
3. Once merged, create a version tag to test production deployment:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
4. Check the **Actions** tab to verify the production deployment

## Troubleshooting

### Authentication Failed
- Verify that WIF_PROVIDER and WIF_SERVICE_ACCOUNT are correctly set
- Check that the service account has the necessary IAM roles
- Ensure the Workload Identity binding includes your repository

### Image Push Failed
- Verify the service account has `artifactregistry.writer` role
- Check that the Artifact Registry repository exists
- Ensure the Docker image path matches your registry

### Deployment Failed
- Verify the service account has `run.admin` and `iam.serviceAccountUser` roles
- Check Cloud Run service quotas
- Review deployment logs in Google Cloud Console
