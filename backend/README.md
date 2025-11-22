# Stock Performance Comparison Tool - Backend

FastAPI-based backend for analyzing and comparing stock performance metrics.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   ├── requests.py      # Request schemas
│   │   └── responses.py     # Response schemas
│   └── routers/             # API route handlers
│       ├── __init__.py
│       ├── health.py        # Health check endpoint
│       └── analytics.py     # Stock analysis endpoints
├── requirements.txt         # Python dependencies
└── README.md
```

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running Locally

Start the development server with auto-reload:

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API Base URL:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

## API Endpoints

### Health Check
```
GET /health
```

Returns API health status, version, and timestamp.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-11-22T12:00:00Z",
  "version": "1.0.0"
}
```

### Stock Analysis (Placeholder)
```
POST /api/analyze
```

Analyzes stock performance for multiple tickers.

**Request Body:**
```json
{
  "tickers": ["AAPL", "GOOGL", "MSFT"],
  "date_range": {
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  },
  "interval": "1d"
}
```

**Response:**
```json
{
  "request_id": "abc123xyz",
  "tickers": ["AAPL", "GOOGL", "MSFT"],
  "metrics": { ... },
  "correlation_matrix": { ... },
  "cached": false,
  "timestamp": "2023-11-22T12:00:00Z"
}
```

## Testing

Run tests with pytest:

```bash
pytest -v --tb=no          # All tests
pytest tests/test_lambda.py -v --tb=no  # Lambda tests only
```

## Features Implemented

### Task 2: FastAPI Skeleton (Complete)
- FastAPI application with health endpoint
- Pydantic models for request/response validation
- Basic routing structure
- Comprehensive test suite

### Task 3: Yahoo Finance Data Fetcher (Complete)
- Fetch historical OHLCV data for single or multiple tickers
- Support for multiple intervals (1d, 1wk, 1mo)
- Robust error handling for invalid tickers
- Ticker validation and information retrieval
- Comprehensive test coverage

### Task 4: Analytics Calculations (Complete)
- Daily returns calculation
- Total return over period
- Volatility (standard deviation of returns)
- Correlation matrix (pairwise between stocks)
- Moving averages (SMA 20/50/200)
- Average trading volume
- Volume trend detection

### Task 5: S3 Caching Layer (Complete)
- S3-based caching with boto3
- Cache key generation (MD5 hash of parameters)
- TTL support (default 24 hours, configurable)
- Automatic cache hit/miss detection
- Cache expiration handling
- Cache management endpoints (stats, clear)
- Environment-based configuration

## Demo & Testing

### Run Yahoo Finance Demo

To see the Yahoo Finance integration in action:

```bash
python demo_yahoo_finance.py
```

This will demonstrate:
- Fetching single ticker data
- Fetching multiple tickers
- Ticker validation
- Getting ticker information
- Different time intervals
- Error handling

### Run API Demo

Start the server and test the API:

```bash
python run_dev.py
```

Then visit http://localhost:8000/docs and try the `/api/analyze` endpoint with:

```json
{
  "tickers": ["AAPL", "GOOGL", "MSFT"],
  "date_range": {
    "start_date": "2025-11-01",
    "end_date": "2025-11-20"
  },
  "interval": "1d"
}
```

The response will include:
- Total return percentage
- Volatility (std dev of returns)
- Average trading volume
- Moving averages (SMA 20, 50, 200)
- Correlation matrix between stocks

## Configuration

Set environment variables to configure caching:

```bash
# Enable/disable caching
export ENABLE_CACHE=true

# S3 bucket for cache
export CACHE_BUCKET_NAME=your-bucket-name

# Cache TTL in hours
export CACHE_TTL_HOURS=24

# AWS region
export AWS_REGION=us-east-1

# For local dev without S3
export USE_LOCAL_CACHE=false
```

## Cache Endpoints

**Get cache stats:**
```
GET /api/cache/stats
```

**Clear all cache:**
```
DELETE /api/cache/clear
```

### Task 6: Lambda Deployment (Complete)
- Mangum wrapper for Lambda
- Lambda handler implementation
- Deployment package creation script
- Lambda configuration (timeout, memory, env vars)
- IAM policy for S3 access
- Deployment script

## Lambda Deployment

### Create Deployment Package

```bash
python deploy_lambda.py
```

This creates `dist/lambda_deployment.zip` with all dependencies.

### Deploy to AWS

**Option 1: Using AWS CLI**

```bash
# Update existing function
aws lambda update-function-code \
  --function-name stock-performance-analyzer \
  --zip-file fileb://dist/lambda_deployment.zip
```

**Option 2: Using deployment script**

```bash
cd ../infra
./deploy.sh
```

### Lambda Configuration

- **Runtime:** Python 3.11
- **Handler:** `lambda_handler.handler`
- **Timeout:** 30 seconds (recommended)
- **Memory:** 512 MB (adjust based on usage)
- **Environment Variables:** See `.env.example`

### IAM Permissions

Lambda needs:
- CloudWatch Logs (write)
- S3 (read/write for cache bucket)

See `infra/iam_policy.json` for complete policy.

## All Tasks Complete

Backend implementation finished:
- Task 2: FastAPI Skeleton
- Task 3: Yahoo Finance Data Fetcher
- Task 4: Analytics Calculations
- Task 5: S3 Caching Layer
- Task 6: Lambda Deployment

## Development Notes

- All ticker symbols are automatically converted to uppercase
- Date validation ensures end_date is after start_date
- CORS is configured for frontend integration
- Request/response models use Pydantic for validation
- Comprehensive API documentation available at `/docs`

