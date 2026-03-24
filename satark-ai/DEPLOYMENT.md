# 🚀 Deploying Satark.ai to Google Cloud

This guide will help you deploy the Satark.ai application to Google Cloud Run.

## Prerequisites

1. **Google Cloud Account** - [Sign up here](https://cloud.google.com/)
2. **gcloud CLI** - [Install here](https://cloud.google.com/sdk/docs/install)
3. **Docker** (optional, for local testing)

## Quick Deployment (Recommended)

### Step 1: Install and Configure Google Cloud CLI

```powershell
# Install gcloud CLI (Windows)
# Download from: https://cloud.google.com/sdk/docs/install

# After installation, initialize
gcloud init

# Login to your Google account
gcloud auth login

# Set your project (create one if needed at console.cloud.google.com)
gcloud config set project YOUR_PROJECT_ID
```

### Step 2: Enable Required APIs

```powershell
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 3: Deploy with One Command

From the `satark-ai` directory:

```powershell
# Option 1: Using Cloud Build (from source)
gcloud run deploy satark-ai `
    --source . `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --port 8080 `
    --memory 2Gi `
    --cpu 2 `
    --set-env-vars GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
```

**Important:** Replace `YOUR_GOOGLE_API_KEY_HERE` with your actual Google API key from the `.env` file.

### Step 4: Access Your App

After deployment completes, you'll see a URL like:
```
https://satark-ai-xxxxxxxxxx-uc.a.run.app
```

Open this URL in your browser to access your deployed app!

## Alternative: Deploy Using Docker

### Step 1: Build Docker Image

```powershell
# Build the image
docker build -t satark-ai .

# Test locally
docker run -p 8080:8080 -e GOOGLE_API_KEY="YOUR_API_KEY" satark-ai
# Visit http://localhost:8080
```

### Step 2: Push to Google Container Registry

```powershell
# Tag the image
docker tag satark-ai gcr.io/YOUR_PROJECT_ID/satark-ai

# Configure Docker for GCR
gcloud auth configure-docker

# Push the image
docker push gcr.io/YOUR_PROJECT_ID/satark-ai
```

### Step 3: Deploy to Cloud Run

```powershell
gcloud run deploy satark-ai `
    --image gcr.io/YOUR_PROJECT_ID/satark-ai `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --port 8080 `
    --memory 2Gi `
    --cpu 2 `
    --set-env-vars GOOGLE_API_KEY="YOUR_API_KEY"
```

## Managing Environment Variables

### Update Environment Variables

```powershell
gcloud run services update satark-ai `
    --region us-central1 `
    --set-env-vars GOOGLE_API_KEY="NEW_API_KEY"
```

### Use Secret Manager (More Secure)

```powershell
# Create secret
echo -n "YOUR_API_KEY" | gcloud secrets create google-api-key --data-file=-

# Grant access to Cloud Run
gcloud secrets add-iam-policy-binding google-api-key `
    --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com `
    --role=roles/secretmanager.secretAccessor

# Deploy with secret
gcloud run deploy satark-ai `
    --source . `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --set-secrets=GOOGLE_API_KEY=google-api-key:latest
```

## Configuration Options

### Adjust Resources

```powershell
# Update memory and CPU
gcloud run services update satark-ai `
    --region us-central1 `
    --memory 1Gi `
    --cpu 1
```

### Set Request Timeout

```powershell
gcloud run services update satark-ai `
    --region us-central1 `
    --timeout 300
```

### Auto-scaling Settings

```powershell
gcloud run services update satark-ai `
    --region us-central1 `
    --min-instances 0 `
    --max-instances 10
```

## Troubleshooting

### View Logs

```powershell
# View recent logs
gcloud run services logs read satark-ai --region us-central1 --limit 50

# Stream logs
gcloud run services logs tail satark-ai --region us-central1
```

### Check Service Details

```powershell
gcloud run services describe satark-ai --region us-central1
```

### Delete Service

```powershell
gcloud run services delete satark-ai --region us-central1
```

## Cost Optimization

Cloud Run pricing:
- **Free tier**: 2 million requests/month
- **Pay per use**: Only charged when handling requests
- **Estimated cost**: ~$0-10/month for moderate traffic

Tips:
- Set `--min-instances 0` to scale to zero when not in use
- Use `--max-instances` to cap costs
- Monitor usage in [Google Cloud Console](https://console.cloud.google.com/)

## Regions

Available regions:
- `us-central1` (Iowa) - Recommended
- `us-east1` (South Carolina)
- `europe-west1` (Belgium)
- `asia-south1` (Mumbai)
- [More regions](https://cloud.google.com/run/docs/locations)

Choose the region closest to your users for best performance.

## CI/CD with GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Cloud SDK
        uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}
      
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy satark-ai \
            --source . \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated \
            --set-env-vars GOOGLE_API_KEY="${{ secrets.GOOGLE_API_KEY }}"
```

## Support

For issues, check:
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Streamlit on Cloud Run](https://docs.streamlit.io/knowledge-base/tutorials/deploy/gcp)
- [Project Issues](https://github.com/imcoderdev/satark-ai/issues)
