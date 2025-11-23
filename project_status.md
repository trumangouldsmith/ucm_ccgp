# Stock Performance Analyzer - Project Status

**Project:** Stock Performance Comparison Tool  
**Team:** Tanner Hughes, Shailesh Dwivedi, Truman Gouldsmith  
**Last Updated:** November 23, 2025

## Current Status: Phase 4 (AWS Infrastructure) - In Progress

### Completed Tasks ✓

**Backend (Tasks 2-6) - COMPLETE**
- FastAPI with health endpoint, analytics endpoint
- Yahoo Finance integration (OHLCV data, all intervals: 5m-1mo)
- Analytics: returns, volatility, correlations, SMAs, volume trends
- S3 caching with TTL (boto3 integration)
- Lambda handler with Mangum wrapper
- 70+ passing tests

**Frontend (Tasks 7-10) - COMPLETE**
- React app (Vite) with routing
- Input form: multi-ticker, date range, interval selector
- Recharts visualization: price line chart, volume bar chart
- Tables: metrics, correlation matrix with color coding
- Axios API integration with error handling
- Health check indicator

**Infrastructure (Task 11) - COMPLETE**
- S3 bucket (frontend): `stock-analyzer-frontend-656312098098`
- S3 bucket (cache): `stock-analyzer-cache-656312098098`
- Frontend bucket: public read enabled, static website hosting enabled
- Cache bucket: private

**Task 12: CloudFront Deployment - COMPLETE** ✓
- Frontend deployed to S3
- CloudFront distribution: `d14pj7ifack6e8.cloudfront.net`
- S3 website URL: `http://stock-analyzer-frontend-656312098098.s3-website-us-east-1.amazonaws.com/`
- **Known Issue:** Frontend shows localhost:8000 connection error (expected - needs API Gateway URL)
- **Action After Task 13:** Rebuild frontend with production API URL

**Lambda Function Name - VERIFIED** ✓
- Function name in AWS: `stock-performance-analyzer` (correct spelling)
- Codebase already using correct name, no changes needed

**Task 13: API Gateway - COMPLETE** ✓
- REST API created: `stock-performance-api`
- Endpoints: /, /health, /api/analyze, /api/cache/stats, /api/cache/clear
- Invoke URL: `https://r58g1ifabj.execute-api.us-east-1.amazonaws.com/prod`
- Lambda proxy integration configured
- CORS enabled on all resources

**Task 14: Lambda Deployment - COMPLETE** ✓
- Deployment package built using `build_lambda_simple.py`
- Using AWS Lambda Layer for pandas/numpy/boto3
- FastAPI 0.88.0 + pydantic 1.10.7 (pure Python)
- Uploaded via S3 and deployed to Lambda
- Runtime: Python 3.11
- Handler: `lambda_handler.handler`
- Environment variables configured
- Health check and API endpoints working

**Frontend Production Deployment - COMPLETE** ✓
- Built with production API URL
- Deployed to S3: `stock-analyzer-frontend-656312098098`
- CloudFront cache invalidated
- Live at: `https://d14pj7ifack6e8.cloudfront.net`
- API connected and working

### In Progress

**Task 15:** CloudWatch Monitoring (NEXT)

### Pending Tasks

- Task 15: CloudWatch monitoring (logs, dashboards, alarms)
- Tasks 16-20: Testing, documentation, presentation

**Known Limitations:**
- Yahoo Finance may block AWS Lambda IPs (rate limiting)
- For demo, use older date ranges (e.g., Oct 2024)

---

## How to Validate Current Setup

### Local Development (Should Work)

**Backend:**
```bash
cd backend
venv\Scripts\activate
set ENABLE_CACHE=false
python run_dev.py
# Should run on http://localhost:8000
# Visit http://localhost:8000/docs for API docs
```

**Frontend:**
```bash
cd frontend
npm run dev
# Should run on http://localhost:5173
# Green "✓ API Connected" indicator in bottom-right = backend running
```

**Full Stack Test:**
1. Start both backend and frontend
2. Enter tickers: AAPL, GOOGL, MSFT
3. Date range: Recent dates (e.g., 2025-11-01 to 2025-11-20)
4. Interval: 1d (or 15m for recent dates)
5. Click "Analyze Stocks"
6. Should see: price chart, metrics table, correlation matrix, volume chart

### Backend Tests
```bash
cd backend
pytest -v --tb=no
# All 70+ tests should pass
```

---

## Key Configuration

### Backend Environment Variables
```
ENABLE_CACHE=false  # For local dev (set to true when Lambda deployed)
CACHE_BUCKET_NAME=stock-analyzer-cache-656312098098
AWS_REGION=us-east-1
```

### Frontend Environment Variables
```
VITE_API_URL=http://localhost:8000  # Local
# VITE_API_URL=https://your-api-gateway-url  # Production (after Task 13)
```

---

## Project Structure

```
ucm_ccgp/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app
│   │   ├── config.py                  # Environment config
│   │   ├── models/                    # Pydantic models
│   │   ├── routers/                   # API endpoints
│   │   │   ├── health.py
│   │   │   └── analytics.py           # /api/analyze
│   │   └── services/
│   │       ├── yahoo_finance.py       # Data fetcher
│   │       ├── analytics.py           # Calculations
│   │       └── cache.py               # S3 caching
│   ├── tests/                         # 70+ tests
│   ├── lambda_handler.py              # Lambda entry point
│   ├── deploy_lambda.py               # Build deployment package
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── HealthCheck.jsx
│   │   │   ├── PriceChart.jsx         # Recharts line chart
│   │   │   ├── VolumeChart.jsx        # Recharts bar chart
│   │   │   ├── MetricsTable.jsx
│   │   │   └── CorrelationMatrix.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx               # Input form
│   │   │   └── Results.jsx            # Charts + metrics
│   │   └── services/
│   │       └── api.js                 # Axios wrapper
│   └── package.json
│
└── infra/
    ├── lambda_config.json             # Lambda settings
    ├── iam_policy.json                # IAM permissions
    └── deploy.sh                      # Deployment script
```

---

## API Endpoints

**Base URL (Local):** http://localhost:8000

**Health Check:**
- `GET /health` - API status

**Analytics:**
- `POST /api/analyze` - Stock analysis
  - Body: `{ tickers: [], date_range: {}, interval: "" }`
  - Returns: metrics, correlation_matrix, historical_data

**Cache Management:**
- `GET /api/cache/stats` - Cache statistics
- `DELETE /api/cache/clear` - Clear cache

---

## AWS Resources Created

**S3 Buckets:**
- Frontend: `stock-analyzer-frontend-656312098098` (public, website hosting)
- Cache: `stock-analyzer-cache-656312098098` (private, Lambda cache storage)

**CloudFront:**
- Distribution: `d14pj7ifack6e8.cloudfront.net`
- Origin: S3 frontend bucket
- HTTPS enabled

**API Gateway:**
- API: `stock-performance-api` (REST API)
- Stage: `prod`
- URL: `https://r58g1ifabj.execute-api.us-east-1.amazonaws.com/prod`

**Lambda:**
- Function: `stock-performance-analyzer`
- Runtime: Python 3.11
- Handler: `lambda_handler.handler`
- Memory: 512 MB, Timeout: 30s
- Layer: AWSSDKPandas-Python311:13 (pandas, numpy, boto3)
- Environment: ENABLE_CACHE=true, CACHE_BUCKET_NAME, AWS_REGION

**Pending:**
- CloudWatch dashboard (Task 15 - optional)

---

## Next Steps

**Task 15: CloudWatch Monitoring (Optional but Recommended)**
1. Enable detailed Lambda logs
2. Create CloudWatch dashboard with:
   - Lambda invocations, errors, duration
   - API Gateway latency, 4xx/5xx errors
   - S3 cache hit/miss metrics
3. Set up alarms for errors/timeouts

**Tasks 16-17: Testing**
- Test multiple stock combinations
- Test different date ranges and intervals
- Validate analytics calculations
- Test cache functionality
- Load testing (if needed)

**Tasks 18-20: Documentation & Presentation**
- Architecture diagram
- Deployment guide
- Demo script
- Presentation slides

---

## Live URLs

**Frontend:** https://d14pj7ifack6e8.cloudfront.net  
**API:** https://r58g1ifabj.execute-api.us-east-1.amazonaws.com/prod

**Test in browser (incognito mode recommended):**
- Enter tickers: AAPL, MSFT
- Date range: 2024-10-01 to 2024-11-01
- Interval: 1d
- Click "Analyze Stocks"

---

## Team Member Checklist

**To verify teammate's work:**
- [ ] Can run backend locally (python run_dev.py)
- [ ] Can run frontend locally (npm run dev)
- [ ] Can access http://localhost:8000/docs
- [ ] Can analyze stocks end-to-end locally
- [ ] All tests pass (pytest -v --tb=no)
- [ ] S3 buckets exist and are configured correctly
- [ ] Have AWS access to the account

**To continue from where we left off:**
- Ready for Task 12: Deploy to S3 + CloudFront
- Backend code is Lambda-ready (lambda_handler.py exists)
- Frontend .env needs API Gateway URL (after Task 13)

---

## Known Limitations

- Intraday intervals (5m, 15m, 30m, 1h) only work for recent dates (Yahoo Finance limitation)
- Cache disabled for local dev (enable after Lambda deployment)
- CORS currently allows all origins (restrict in production)

## Dependencies

**Backend:** Python 3.8+, FastAPI, pandas, yfinance, boto3, mangum  
**Frontend:** Node 18+, React, Recharts, Axios, React Router  
**AWS:** S3, CloudFront, API Gateway, Lambda, CloudWatch, IAM

