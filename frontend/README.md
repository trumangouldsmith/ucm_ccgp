# Stock Performance Analyzer - Frontend

React frontend for the Stock Performance Comparison Tool.

## Features

- Stock ticker input (multi-select)
- Date range selection
- Interval selection (daily/weekly/monthly)
- Results visualization (Tasks 8-9)
- API integration (Task 10)

## Development

```bash
npm install
npm run dev
```

Visit http://localhost:5173

## Build

```bash
npm run build
```

Output in `dist/` folder, ready for S3 deployment.

## Tasks Complete

- Task 7: React app setup with routing and layout
- Task 8: Input interface (complete with validation)
- Task 9: Display metrics & charts
  - Price performance line chart
  - Trading volume bar chart
  - Metrics table (returns, volatility, volume)
  - Correlation matrix with color coding

## Pending

- Task 10: Connect to backend API (currently using mock data)
