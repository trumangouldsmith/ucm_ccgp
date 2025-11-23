# Task 13: Configure API Gateway

## Step-by-Step AWS Console Instructions

### Part 1: Create REST API

1. **Open API Gateway Console**
   - Go to AWS Console → Services → API Gateway
   - Click **Create API**

2. **Choose REST API**
   - Find "REST API" (NOT Private or HTTP API)
   - Click **Build**

3. **Configure API**
   - Protocol: **REST**
   - Create new API: **New API**
   - API name: `stock-performance-api`
   - Description: `Stock Performance Comparison API`
   - Endpoint Type: **Regional**
   - Click **Create API**

---

### Part 2: Create Resources & Methods

#### A. Setup Root / Endpoint (Optional but Recommended)

1. **Create GET Method on Root**
   - Select root `/`
   - Click **Actions** → **Create Method**
   - Choose **GET** from dropdown
   - Click checkmark ✓
   - Integration type: **Lambda Function**
   - Use Lambda Proxy integration: **Check this box** ✓
   - Lambda Region: `us-east-1`
   - Lambda Function: `stock-performance-analyzer`
   - Click **Save** → **OK**

#### B. Create /health Endpoint

1. **Create Resource**
   - Select root `/`
   - Click **Actions** → **Create Resource**
   - Resource Name: `health`
   - Resource Path: `/health`
   - Enable API Gateway CORS: **Check this box**
   - Click **Create Resource**

2. **Create GET Method**
   - Select `/health` resource
   - Click **Actions** → **Create Method**
   - Choose **GET** from dropdown
   - Click the checkmark ✓

3. **Configure GET Method**
   - Integration type: **Lambda Function**
   - Use Lambda Proxy integration: **Check this box** ✓
   - Lambda Region: `us-east-1`
   - Lambda Function: `stock-performance-analyzer`
   - Click **Save**
   - Click **OK** when prompted to give API Gateway permission

#### C. Create /api Resource

1. **Create /api Resource**
   - Select root `/` 
   - Click **Actions** → **Create Resource**
   - Resource Name: `api`
   - Resource Path: `/api`
   - Enable API Gateway CORS: **Check this box**
   - Click **Create Resource**

#### D. Create /api/analyze Endpoint

1. **Create Resource**
   - Select `/api` resource
   - Click **Actions** → **Create Resource**
   - Resource Name: `analyze`
   - Resource Path: `/api/analyze`
   - Enable API Gateway CORS: **Check this box**
   - Click **Create Resource**

2. **Create POST Method**
   - Select `/api/analyze` resource
   - Click **Actions** → **Create Method**
   - Choose **POST** from dropdown
   - Click checkmark ✓

3. **Configure POST Method**
   - Integration type: **Lambda Function**
   - Use Lambda Proxy integration: **Check this box** ✓
   - Lambda Region: `us-east-1`
   - Lambda Function: `stock-performance-analyzer`
   - Click **Save**
   - Click **OK** when prompted

#### E. Create /api/cache/stats Endpoint

1. **Create /cache Resource**
   - Select `/api` resource
   - Click **Actions** → **Create Resource**
   - Resource Name: `cache`
   - Resource Path: `/api/cache`
   - Enable API Gateway CORS: **Check this box**
   - Click **Create Resource**

2. **Create /stats Resource**
   - Select `/api/cache` resource
   - Click **Actions** → **Create Resource**
   - Resource Name: `stats`
   - Resource Path: `/api/cache/stats`
   - Enable API Gateway CORS: **Check this box**
   - Click **Create Resource**

3. **Create GET Method**
   - Select `/api/cache/stats` resource
   - Click **Actions** → **Create Method**
   - Choose **GET** from dropdown
   - Click checkmark ✓
   - Integration type: **Lambda Function**
   - Use Lambda Proxy integration: **Check this box** ✓
   - Lambda Region: `us-east-1`
   - Lambda Function: `stock-performance-analyzer`
   - Click **Save** → **OK**

#### F. Create /api/cache/clear Endpoint

1. **Create /clear Resource**
   - Select `/api/cache` resource
   - Click **Actions** → **Create Resource**
   - Resource Name: `clear`
   - Resource Path: `/api/cache/clear`
   - Enable API Gateway CORS: **Check this box**
   - Click **Create Resource**

2. **Create DELETE Method**
   - Select `/api/cache/clear` resource
   - Click **Actions** → **Create Method**
   - Choose **DELETE** from dropdown
   - Click checkmark ✓
   - Integration type: **Lambda Function**
   - Use Lambda Proxy integration: **Check this box** ✓
   - Lambda Region: `us-east-1`
   - Lambda Function: `stock-performance-analyzer`
   - Click **Save** → **OK**

---

### Part 3: Deploy API

1. **Deploy to Stage**
   - Click **Actions** → **Deploy API**
   - Deployment stage: **[New Stage]**
   - Stage name: `prod`
   - Stage description: `Production`
   - Click **Deploy**

2. **Get API URL**
   - After deployment, you'll see **Invoke URL** at top of stage editor
   - Example: `https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod`
   - **COPY THIS URL** - you'll need it for frontend

---

### Part 4: Enable CORS (Additional Configuration)

If you checked "Enable API Gateway CORS" when creating resources, this is mostly done. But verify:

1. **For each endpoint** (`/health`, `/api/analyze`, etc.):
   - Select the resource
   - You should see an **OPTIONS** method (auto-created)
   - If not, manually enable CORS:
     - Select resource
     - Click **Actions** → **Enable CORS**
     - Keep default settings
     - Click **Enable CORS and replace existing CORS headers**

2. **Re-deploy after CORS changes**
   - Click **Actions** → **Deploy API**
   - Select stage: `prod`
   - Click **Deploy**

---

## Verification Steps

### Test the API

1. **Test /health endpoint**
   ```bash
   curl https://YOUR_API_URL/prod/health
   ```
   Expected response:
   ```json
   {"status":"healthy","message":"Stock Performance Analyzer API"}
   ```

2. **Test /api/analyze endpoint**
   ```bash
   curl -X POST https://YOUR_API_URL/prod/api/analyze \
     -H "Content-Type: application/json" \
     -d '{
       "tickers": ["AAPL", "GOOGL"],
       "date_range": {"start_date": "2025-11-01", "end_date": "2025-11-20"},
       "interval": "1d"
     }'
   ```
   Should return stock analysis data.

### Test from Browser Console

Open browser console on CloudFront site and run:

```javascript
fetch('https://YOUR_API_URL/prod/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

Should log: `{status: "healthy", message: "..."}`

---

## Expected Structure

Your API Gateway should have this structure:

```
/ (root)
├── GET → Lambda (API info)
├── /health
│   ├── GET → Lambda
│   └── OPTIONS (CORS)
└── /api
    ├── /analyze
    │   ├── POST → Lambda
    │   └── OPTIONS (CORS)
    └── /cache
        ├── /stats
        │   ├── GET → Lambda
        │   └── OPTIONS (CORS)
        └── /clear
            ├── DELETE → Lambda
            └── OPTIONS (CORS)
```

---

## Common Issues

**Issue: CORS errors in browser**
- Solution: Re-enable CORS on all resources, redeploy to `prod` stage

**Issue: 403 Forbidden**
- Solution: Check Lambda has proper IAM role with S3 permissions

**Issue: 502 Bad Gateway**
- Solution: Check Lambda timeout (should be 30s), check Lambda logs in CloudWatch

**Issue: Lambda not receiving requests**
- Solution: Verify "Use Lambda Proxy integration" is enabled for all methods

---

## After Completion

You'll have:
- API Gateway URL: `https://[ID].execute-api.us-east-1.amazonaws.com/prod`

**Save this URL!** You need it for:
1. Updating frontend environment variable
2. Testing the full stack
3. Task 14 validation

---

## Quick Reference: Endpoints to Create

Copy this checklist as you create each endpoint:

- [ ] `GET /` → Lambda (stock-performance-analyzer, proxy integration)
- [ ] `GET /health` → Lambda (stock-performance-analyzer, proxy integration, CORS)
- [ ] `POST /api/analyze` → Lambda (stock-performance-analyzer, proxy integration, CORS)
- [ ] `GET /api/cache/stats` → Lambda (stock-performance-analyzer, proxy integration, CORS)
- [ ] `DELETE /api/cache/clear` → Lambda (stock-performance-analyzer, proxy integration, CORS)
- [ ] Deploy to stage: `prod`
- [ ] Copy Invoke URL

