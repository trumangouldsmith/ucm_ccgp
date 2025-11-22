Online Group 2
Stock Performance Comparison Tool
Group Members:
Tanner Hughes
Shailesh Dwivedi
Truman Gouldsmith

Overview:
The Stock Performance Comparison Tool is a financial analytics platform that allows investors and analysts to compare the performance of multiple publicly traded companies across chosen timeframes. The application provides interactive metrics such as returns, volatility, correlation, moving averages, and trading volume.

Abstract
This application enables users to select multiple stock symbols, define custom time ranges, and visualize performance metrics through a web interface. The backend, implemented using FastAPI and deployed via AWS Lambda, retrieves data dynamically from Yahoo Finance’s public API. It processes the data in-memory, calculates comparative metrics, and returns the results to the frontend.

The frontend is a static single-page web app (React) hosted in Amazon S3, distributed globally through Amazon CloudFront. Data persistence and caching use Amazon S3, while Amazon API Gateway securely manages communication between the frontend and the Lambda backend. System monitoring and performance visibility are provided through Amazon CloudWatch.
This project highlights how AWS’s serverless ecosystem can support financial data analytics with minimal management overhead and high scalability.


Outline of Architecture and Data Trajectory:
Amazon S3 (Frontend Hosting and Data Cache)
Hosts the React single-page application (SPA) as a static website.
Serves static frontend files distributed globally through CloudFront.
Stores cached stock data and computed analytics for faster repeat access and reduced API calls.
Requires proper bucket policy for public static website hosting and secure read/write access for Lambda.
Amazon CloudFront (Content Delivery Network)
Provides global, low-latency delivery of the React frontend hosted on S3.
Enables HTTPS and caching at edge locations to reduce load times for users.
Enhances security through SSL/TLS encryption and optionally integrates with AWS WAF for protection.
Requires configuration to point origin to the S3 frontend bucket and caching policies tailored to SPA needs.
AWS API Gateway
Acts as a RESTful interface exposing the backend Lambda functions to the frontend securely
Manages API request throttling, authorization (can integrate with Cognito or API keys), and monitoring.
Converts HTTPS requests from the React frontend into Lambda invocations.
Requires careful CORS configuration to allow browser-based API calls.
AWS Lambda (Backend, FastAPI)
Implements backend logic using FastAPI framework deployed as serverless Lambda functions.
Fetches stock data from Yahoo Finance public APIs, processes it in-memory to calculate returns, volatility, correlations, moving averages, and volume.
Reads from and writes to S3 for caching API responses and computed results to optimize performance and reduce external API calls
Requires optimization for cold start latency, proper memory allocation, and timeout settings to handle data processing efficiently.
Logs execution metrics and errors to CloudWatch for observability.
Amazon CloudWatch
Collects logs, metrics, and traces from Lambda functions and API Gateway.
Enables monitoring of API performance, error rates, and backend health.
Supports setting alarms and automated responses for failures or performance degradation.
Requires configuration of log retention policies and dashboard creation for actionable insights.
