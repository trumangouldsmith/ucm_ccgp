# Stock Performance Comparison Tool

## Overview

The **Stock Performance Comparison Tool** is a serverless financial analytics platform that lets users compare the performance of multiple publicly traded companies over custom time ranges. Users can visualize metrics such as:

* Returns
* Volatility
* Correlation
* Moving averages
* Trading volume

The system uses a **React frontend**, a **FastAPI backend running on AWS Lambda**, and a fully serverless AWS architecture for scalability and low operational overhead.

---

## Architecture Summary

### **Frontend: React (S3 + CloudFront)**

* React SPA hosted in an S3 bucket
* Distributed globally via CloudFront
* Uses HTTPS via ACM certificates
* Connects to backend through API Gateway

### **Backend: FastAPI on AWS Lambda**

* FastAPI application wrapped for Lambda execution
* Fetches data from Yahoo Finance public API
* Computes performance metrics in-memory
* Reads/writes cached data to S3 to reduce API calls

### **API Gateway**

* REST API exposing Lambda endpoints
* Handles CORS, throttling, and routing

### **Storage & Caching (S3)**

* Frontend S3 bucket for static site hosting
* Backend cache bucket for stock data and computed analytics

### **Monitoring: CloudWatch**

* Logs Lambda executions and API Gateway requests
* Dashboards and alarms for performance and errors

---

# Project Roadmap & Task Plan

Below is a task-oriented, claimable plan so group members can work independently.

---

## Phase 1 — Project Setup

### 1. Repository Initialization

* Create GitHub repo with structure:

  * `/frontend`
  * `/backend`
  * `/infra`
  * `/docs`
* Add README and contribution guidelines

**Claimable by:** Anyone

---

## Phase 2 — Backend (FastAPI + Lambda)

### 2. FastAPI Skeleton

* Create basic FastAPI project
* Add `/health` endpoint
* Add Pydantic models

### 3. Yahoo Finance Data Fetcher

* Fetch OHLCV data for tickers
* Validate ranges
* Handle fetch errors

### 4. Analytics Engine

Implement:

* Daily returns
* Volatility
* Correlation matrix
* SMA (20/50/200)
* Volume stats

### 5. S3 Caching Layer

* Store fetched/calc results in JSON
* Implement TTL policy
* Add S3 read/write logic

### 6. Lambda Deployment

* Use Mangum
* Package FastAPI for Lambda
* Configure IAM role for S3
* Optimize memory/timeouts

**Claimable by:** Backend-focused team member

---

## Phase 3 — Frontend (React SPA)

### 7. React App Setup

* Initialize React (Vite preferred)
* Setup main layout and routing

### 8. Ticker & Date Input UI

* Multi-select input for tickers
* Date range picker
* Validation + loading states

### 9. Data Visualization Components

* Price history chart
* Volume chart
* Metrics table
* Correlation matrix view

### 10. API Connectivity

* Add Axios/fetch wrapper
* Connect to API Gateway endpoint
* Handle errors & retries

**Claimable by:** Frontend-focused team member

---

## Phase 4 — AWS Infrastructure

### 11. S3 Buckets

* Frontend hosting bucket
* Cache bucket (private)
* Bucket policies and CORS

### 12. CloudFront Distribution

* Point to S3 origin
* Configure HTTPS & caching rules
* SPA-friendly 404 behavior

### 13. API Gateway Setup

* Create REST API route `/analyze`
* Integrate with Lambda
* Enable CORS

### 14. Lambda Deployment Pipeline

* Package and upload backend code
* Configure env variables
* Attach IAM permissions

### 15. CloudWatch Monitoring

* Enable logs for Gateway & Lambda
* Create dashboards
* Set alarms for errors or high latency

**Claimable by:** AWS/Infra-focused team member

---

## Phase 5 — Data Quality & Testing

### 16. Analytics Validation

* Cross-check values vs Yahoo Finance
* Validate correlations and SMAs

### 17. Load Testing

* Test cold starts
* Evaluate S3 caching effectiveness
* Simulate multiple ticker requests

### 18. End-to-End Integration

* Confirm frontend ↔ API ↔ Lambda flow
* Validate all CORS and networking

**Claimable by:** Anyone

---

## Phase 6 — Final Delivery

### 19. Documentation

Prepare:

* Architecture diagram
* Deployment instructions
* Local development guide
* API reference docs

### 20. Presentation

* Build demo script
* Prepare slides
* Rehearse live or recorded demo

**Claimable by:** Entire team

---

# How to Run Locally

## Backend

```bash
cd backend
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# Technologies Used

### **Frontend**

* React
* Recharts / Chart.js
* Axios

### **Backend**

* FastAPI
* Pandas / NumPy
* boto3
* Mangum

### **AWS**

* Lambda
* API Gateway
* S3
* CloudFront
* CloudWatch

---

# Team Members

* **Tanner Hughes** — AWS Infrastructure
* **Shailesh Dwivedi** — Backend & Analytics
* **Truman Gouldsmith** — Frontend & Integration

---

If you need, I can also create:

* A polished architecture diagram
* A GitHub Projects board
* A Gantt timeline
* API documentation page

Just tell me!
