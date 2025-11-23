# Task 14: Deploy Lambda Function Code

## Option 1: Manual Upload (Recommended for Windows)

### Step 1: Build Deployment Package

1. **Open terminal in backend directory:**
   ```bash
   cd C:\personal_projects\ucm_ccgp\backend
   ```

2. **Activate virtual environment:**
   ```bash
   venv\Scripts\activate
   ```

3. **Run deployment script:**
   ```bash
   python deploy_lambda.py
   ```

4. **Wait for completion** (creates `dist/lambda_deployment.zip`)

### Step 2: Upload to Lambda via Console

1. **Go to Lambda Console**
   - AWS Console → Lambda → Functions
   - Click `stock-performance-analyzer`

2. **Upload ZIP**
   - Scroll to "Code source" section
   - Click **Upload from** → **.zip file**
   - Click **Upload**
   - Select: `C:\personal_projects\ucm_ccgp\backend\dist\lambda_deployment.zip`
   - Click **Save**
   - Wait for upload (may take 1-2 minutes)

### Step 3: Configure Environment Variables

1. **Go to Configuration tab**
   - Click **Configuration** → **Environment variables**
   - Click **Edit**

2. **Add variables:**
   - `CACHE_BUCKET_NAME` = `stock-analyzer-cache-656312098098`
   - `ENABLE_CACHE` = `true`
   - `AWS_REGION` = `us-east-1`
   - `CACHE_TTL_HOURS` = `24`
   
3. **Click Save**

### Step 4: Verify Lambda Settings

1. **General Configuration**
   - Configuration → General configuration → Edit
   - Timeout: `30 seconds` (not 3 seconds!)
   - Memory: `512 MB`
   - Click **Save**

2. **Runtime**
   - Should be: `Python 3.11`
   - Handler: `lambda_handler.handler`

### Step 5: Test Lambda Function

1. **Create test event**
   - Click **Test** tab
   - Event name: `test-health`
   - Event JSON:
   ```json
   {
     "httpMethod": "GET",
     "path": "/health",
     "headers": {}
   }
   ```
   - Click **Save**

2. **Run test**
   - Click **Test**
   - Should see success with response:
   ```json
   {
     "statusCode": 200,
     "headers": {
       "access-control-allow-origin": "*",
       ...
     },
     "body": "{\"status\":\"healthy\",\"message\":\"Stock Performance Analyzer API\"}"
   }
   ```

### Step 6: Test with Real Data

1. **Create new test event**
   - Event name: `test-analyze`
   - Event JSON:
   ```json
   {
     "httpMethod": "POST",
     "path": "/api/analyze",
     "headers": {
       "Content-Type": "application/json"
     },
     "body": "{\"tickers\":[\"AAPL\"],\"date_range\":{\"start_date\":\"2025-11-01\",\"end_date\":\"2025-11-20\"},\"interval\":\"1d\"}"
   }
   ```
   - Click **Save** → **Test**
   - Should return stock analysis data

---

## Option 2: Using AWS CLI (If Installed)

If you have AWS CLI configured:

```bash
cd C:\personal_projects\ucm_ccgp\backend
python deploy_lambda.py
aws lambda update-function-code --function-name stock-performance-analyzer --zip-file fileb://dist/lambda_deployment.zip --region us-east-1
```

Then configure environment variables in console (Step 3 above).

---

## Verify IAM Permissions

Lambda needs S3 access. Check execution role:

1. **Configuration → Permissions**
2. **Click execution role name** (opens IAM)
3. **Verify policy includes:**
   ```json
   {
     "Effect": "Allow",
     "Action": [
       "s3:GetObject",
       "s3:PutObject",
       "s3:DeleteObject",
       "s3:ListBucket"
     ],
     "Resource": [
       "arn:aws:s3:::stock-analyzer-cache-656312098098",
       "arn:aws:s3:::stock-analyzer-cache-656312098098/*"
     ]
   }
   ```

4. **If missing, add inline policy:**
   - Policies → Add permissions → Create inline policy
   - JSON tab → paste above
   - Name: `S3CacheAccess`
   - Click **Create policy**

---

## Test API Gateway Integration

Now that Lambda has code, test API Gateway again:

**Browser console (on CloudFront site):**
```javascript
fetch('https://r58g1ifabj.execute-api.us-east-1.amazonaws.com/prod/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

**Should return:**
```json
{
  "status": "healthy",
  "message": "Stock Performance Analyzer API"
}
```

**Test analyze endpoint:**
```javascript
fetch('https://r58g1ifabj.execute-api.us-east-1.amazonaws.com/prod/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    tickers: ['AAPL'],
    date_range: { start_date: '2025-11-01', end_date: '2025-11-20' },
    interval: '1d'
  })
})
  .then(r => r.json())
  .then(d => console.log(d))
```

---

## Common Issues

**"Package too large" error:**
- Check ZIP size: should be < 50 MB
- If larger, use Lambda layers for dependencies

**"Internal server error" in API Gateway:**
- Check CloudWatch logs: Lambda → Monitor → View logs in CloudWatch
- Common: timeout (increase to 30s), permissions (add S3 policy)

**CORS errors still present:**
- Verify FastAPI has CORS middleware (it does in `app/main.py`)
- Check Lambda response includes CORS headers in test output

**yfinance errors:**
- Expected for old dates or invalid tickers
- Check CloudWatch logs for details

---

## After Completion

You'll have:
- Lambda function deployed with code ✓
- Environment variables configured ✓
- API Gateway → Lambda working ✓
- CORS headers working ✓

**Next:** Update frontend with API Gateway URL and redeploy

