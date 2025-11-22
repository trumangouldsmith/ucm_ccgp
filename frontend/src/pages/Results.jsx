import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { analyzeStocks } from '../services/api';
import PriceChart from '../components/PriceChart';
import VolumeChart from '../components/VolumeChart';
import MetricsTable from '../components/MetricsTable';
import CorrelationMatrix from '../components/CorrelationMatrix';
import './Results.css';

// Transform backend data to chart format
const transformDataForCharts = (backendData) => {
  const { metrics, correlation_matrix, tickers, historical_data } = backendData;
  
  if (!historical_data) {
    return {
      priceData: [],
      volumeData: [],
      metrics,
      correlationMatrix: correlation_matrix,
      tickers,
      cached: backendData.cached
    };
  }
  
  // Combine all tickers' data by date
  const dateMap = new Map();
  
  tickers.forEach(ticker => {
    const tickerData = historical_data[ticker] || [];
    tickerData.forEach(point => {
      if (!dateMap.has(point.date)) {
        dateMap.set(point.date, { date: point.date });
      }
      const datePoint = dateMap.get(point.date);
      datePoint[ticker] = point.close;
      datePoint[`${ticker}_volume`] = point.volume;
    });
  });
  
  // Convert to sorted arrays
  const priceData = Array.from(dateMap.values()).sort((a, b) => 
    a.date.localeCompare(b.date)
  );
  const volumeData = priceData; // Same data, different fields used
  
  return {
    priceData,
    volumeData,
    metrics,
    correlationMatrix: correlation_matrix,
    tickers,
    cached: backendData.cached
  };
};

function Results() {
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      const tickers = searchParams.get('tickers')?.split(',') || [];
      const startDate = searchParams.get('startDate');
      const endDate = searchParams.get('endDate');
      const interval = searchParams.get('interval') || '1d';
      
      if (tickers.length === 0 || !startDate || !endDate) {
        setError('Invalid parameters');
        setLoading(false);
        return;
      }
      
      try {
        // Call real backend API
        const response = await analyzeStocks({
          tickers,
          startDate,
          endDate,
          interval
        });
        
        // Transform backend data for charts
        const transformedData = transformDataForCharts(response);
        
        setData({
          tickers,
          startDate,
          endDate,
          interval,
          ...transformedData
        });
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    
    fetchData();
  }, [searchParams]);

  if (loading) {
    return (
      <div className="results">
        <div className="loading">Loading analysis...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="results">
        <div className="error">
          <h3>Error</h3>
          <p>{error}</p>
          <Link to="/" className="back-link">← Back to Home</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="results">
      <div className="results-header">
        <h2>Analysis Results</h2>
        <Link to="/" className="back-link">← New Analysis</Link>
      </div>
      
      <div className="results-info">
        <p><strong>Tickers:</strong> {data?.tickers?.join(', ')}</p>
        <p><strong>Period:</strong> {data?.startDate} to {data?.endDate}</p>
        <p><strong>Interval:</strong> {data?.interval}</p>
        {data?.cached && (
          <p className="cache-notice">✓ Results from cache</p>
        )}
      </div>
      
      {data.priceData && data.priceData.length > 0 && (
        <PriceChart data={data.priceData} tickers={data.tickers} />
      )}
      
      <MetricsTable metrics={data.metrics} />
      
      <CorrelationMatrix 
        correlationMatrix={data.correlationMatrix} 
        tickers={data.tickers} 
      />
      
      {data.volumeData && data.volumeData.length > 0 && (
        <VolumeChart data={data.volumeData} tickers={data.tickers} />
      )}
    </div>
  );
}

export default Results;

