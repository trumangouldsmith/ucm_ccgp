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
  // For now, return placeholder since we need historical price data from backend
  // This will be updated when backend returns time series data
  const { metrics, correlation_matrix, tickers } = backendData;
  
  // Placeholder chart data - in production, backend should return historical prices
  const priceData = [];
  const volumeData = [];
  
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
      
      <MetricsTable metrics={data.metrics} />
      
      <CorrelationMatrix 
        correlationMatrix={data.correlationMatrix} 
        tickers={data.tickers} 
      />
    </div>
  );
}

export default Results;

