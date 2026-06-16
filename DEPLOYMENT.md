# 🚀 LuxePricing.ai Deployment Guide

## Table of Contents
1. [Streamlit Cloud (Recommended)](#streamlit-cloud)
2. [Docker & AWS](#docker--aws)
3. [GitHub Actions CI/CD](#github-actions-cicd)
4. [Environment Configuration](#environment-configuration)
5. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Streamlit Cloud

### Prerequisites
- GitHub account with repository access
- Streamlit account (free tier available)

### Steps

1. **Prepare Repository**
   ```bash
   git add .
   git commit -m "Ready for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Visit Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Select your GitHub repo
   - Choose branch: `main`
   - Set script path: `app.py`

3. **Configure Secrets**
   - In Streamlit Cloud dashboard: Settings → Secrets
   - Add your API keys:
     ```toml
     [secrets]
     openai_api_key = "sk-..."
     anthropic_api_key = "sk-ant-..."
     ```

4. **Deploy**
   - Click "Deploy"
   - Wait for build completion (~2-3 minutes)
   - Share URL with team

### URL Format
```
https://<github-username>-luxepricing-ai2-<branch>-<hash>.streamlit.app
```

---

## Docker & AWS

### Build Docker Image

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build & Test Locally

```bash
# Build image
docker build -t luxepricing:latest .

# Run container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY="sk-..." \
  -e ANTHROPIC_API_KEY="sk-ant-..." \
  luxepricing:latest

# Test
curl http://localhost:8501/_stcore/health
```

### Deploy to AWS ECS

```bash
# 1. Push to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker tag luxepricing:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/luxepricing:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/luxepricing:latest

# 2. Create ECS task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# 3. Create service
aws ecs create-service \
  --cluster luxepricing-cluster \
  --service-name luxepricing-app \
  --task-definition luxepricing:1 \
  --desired-count 2

# 4. Update with new image
aws ecs update-service \
  --cluster luxepricing-cluster \
  --service luxepricing-app \
  --force-new-deployment
```

### AWS ECS Task Definition Template

```json
{
  "family": "luxepricing",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "luxepricing",
      "image": "<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/luxepricing:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "hostPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "STREAMLIT_SERVER_HEADLESS",
          "value": "true"
        },
        {
          "name": "STREAMLIT_LOGGER_LEVEL",
          "value": "info"
        }
      ],
      "secrets": [
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:<ACCOUNT_ID>:secret:luxepricing/openai-key"
        },
        {
          "name": "ANTHROPIC_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:<ACCOUNT_ID>:secret:luxepricing/anthropic-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/luxepricing",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8501/_stcore/health || exit 1"],
        "interval": 30,
        "timeout": 10,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

---

## GitHub Actions CI/CD

### Automated Testing & Deployment

```yaml
# .github/workflows/deploy.yml
name: Deploy LuxePricing.ai

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest tests/ --cov=modules --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  deploy:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to AWS
        run: |
          aws ecs update-service \
            --cluster luxepricing-cluster \
            --service luxepricing-app \
            --force-new-deployment
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

---

## Environment Configuration

### Streamlit Secrets (`.streamlit/secrets.toml`)

```toml
[openai]
api_key = "sk-..."
model = "gpt-4"

[anthropic]
api_key = "sk-ant-..."
model = "claude-3-opus"

[database]
url = "postgresql://..."

[hotel]
name = "Luxe Hotel Paris"
market_code = "PAR"
```

### Environment Variables

```bash
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_LOGGER_LEVEL=info
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

## Monitoring & Maintenance

### Health Checks

```bash
# Check Streamlit Cloud status
curl -I https://<your-app>.streamlit.app/

# Monitor logs
streamlit logs --tail 100
```

### Performance Monitoring

- **Page Load Time**: < 3 seconds
- **API Response**: < 500ms
- **Memory Usage**: < 2GB
- **CPU Usage**: < 50%

### Updates & Rollback

```bash
# Deploy new version
git tag v1.1.0
git push origin main v1.1.0

# Rollback if needed
aws ecs update-service \
  --cluster luxepricing-cluster \
  --service luxepricing-app \
  --task-definition luxepricing:1 \
  --force-new-deployment
```

---

## Cost Estimation

| Platform | Monthly Cost | Notes |
|----------|-------------|-------|
| Streamlit Cloud (Free) | $0 | Limited compute |
| Streamlit Cloud (Pro) | $49 | Unlimited compute |
| AWS Fargate | $50-200 | Scalable |
| AWS EC2 | $30-100 | Fixed instance |

---

**For questions or issues, open a GitHub issue or contact support@luxepricing.ai**
