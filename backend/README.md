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
pytest
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

## Next Steps

Ready for:

- **Task 5:** Add S3 caching layer
- **Task 6:** Wrap for AWS Lambda deployment

## Development Notes

- All ticker symbols are automatically converted to uppercase
- Date validation ensures end_date is after start_date
- CORS is configured for frontend integration
- Request/response models use Pydantic for validation
- Comprehensive API documentation available at `/docs`

