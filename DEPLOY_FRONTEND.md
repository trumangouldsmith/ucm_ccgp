# Deploy Frontend to S3/CloudFront

## Step 1: Build with Production API URL

```bash
cd C:\personal_projects\ucm_ccgp\frontend
npm run build
```

This creates `dist/` folder with production build using API Gateway URL.

## Step 2: Upload to S3

**Manual Upload:**

1. Go to S3 Console → `stock-analyzer-frontend-656312098098`
2. **Delete old files** (select all → Delete)
3. Click **Upload**
4. **Add files** → Select ALL files from `frontend\dist\` folder
   - Include: `index.html`, `assets/` folder, `vite.svg`, etc.
5. Click **Upload**

**Important:** Upload files directly to bucket root, NOT in a subfolder.

## Step 3: Invalidate CloudFront Cache

1. Go to CloudFront Console
2. Find distribution: `d14pj7ifack6e8.cloudfront.net`
3. Click distribution ID
4. Go to **Invalidations** tab
5. Click **Create invalidation**
6. Object paths: `/*`
7. Click **Create invalidation**
8. Wait 1-2 minutes for completion

## Step 4: Test

Visit: `https://d14pj7ifack6e8.cloudfront.net`

- Should see green "✓ API Connected" indicator
- Try analyzing stocks: AAPL, MSFT
- Date range: 2024-10-01 to 2024-11-01
- Interval: 1d
- Click "Analyze Stocks"

Should work end-to-end!

---

## Troubleshooting

**API indicator still red:**
- Check browser console for errors
- Verify .env.production has correct API URL
- Rebuild: `npm run build`
- Re-upload to S3
- Invalidate CloudFront cache again

**404 errors on refresh:**
- CloudFront needs error page routing
- Distribution → Error pages → Create custom error response
- HTTP error code: 404
- Response page path: `/index.html`
- HTTP response code: 200

