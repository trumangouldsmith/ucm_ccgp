import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import PriceChart from '../components/PriceChart';
import VolumeChart from '../components/VolumeChart';
import MetricsTable from '../components/MetricsTable';
import CorrelationMatrix from '../components/CorrelationMatrix';
import './Results.css';

// Mock data generator for demo
const generateMockData = (tickers, startDate, endDate) => {
  const start = new Date(startDate);
  const end = new Date(endDate);
  const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
  
  const priceData = [];
  const volumeData = [];
  const metrics = {};
  const correlationMatrix = {};
  
  // Generate price and volume data
  for (let i = 0; i <= days; i++) {
    const date = new Date(start);
    date.setDate(start.getDate() + i);
    const dateStr = date.toISOString().split('T')[0];
    
    const pricePoint = { date: dateStr };
    const volumePoint = { date: dateStr };
    
    tickers.forEach((ticker, index) => {
      const basePrice = 100 + index * 50;
      const trend = i * (0.5 + index * 0.3);
      const volatility = Math.random() * 10 - 5;
      pricePoint[ticker] = basePrice + trend + volatility;
      volumePoint[`${ticker}_volume`] = Math.floor(1000000 + Math.random() * 5000000);
    });
    
    priceData.push(pricePoint);
    volumeData.push(volumePoint);
  }
  
  // Generate metrics
  tickers.forEach((ticker, index) => {
    metrics[ticker] = {
      total_return: (5 + index * 3) * (Math.random() > 0.3 ? 1 : -1),
      volatility: 1.2 + index * 0.4 + Math.random(),
      average_volume: 1500000 + index * 500000 + Math.floor(Math.random() * 1000000)
    };
  });
  
  // Generate correlation matrix
  tickers.forEach((ticker1, i) => {
    correlationMatrix[ticker1] = {};
    tickers.forEach((ticker2, j) => {
      if (i === j) {
        correlationMatrix[ticker1][ticker2] = 1.0;
      } else if (i < j) {
        const corr = Math.random() * 1.6 - 0.3; // Range: -0.3 to 1.3
        const bounded = Math.max(-1, Math.min(1, corr));
        correlationMatrix[ticker1][ticker2] = bounded;
        if (!correlationMatrix[ticker2]) correlationMatrix[ticker2] = {};
        correlationMatrix[ticker2][ticker1] = bounded;
      }
    });
  });
  
  return { priceData, volumeData, metrics, correlationMatrix };
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
      
      // Simulate API call with mock data
      try {
        await new Promise(resolve => setTimeout(resolve, 800));
        
        const mockData = generateMockData(tickers, startDate, endDate);
        
        setData({
          tickers,
          startDate,
          endDate,
          interval,
          ...mockData
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
        <p className="mock-notice">Note: Currently showing mock data. Backend integration in Task 10.</p>
      </div>
      
      <PriceChart data={data.priceData} tickers={data.tickers} />
      
      <MetricsTable metrics={data.metrics} />
      
      <CorrelationMatrix 
        correlationMatrix={data.correlationMatrix} 
        tickers={data.tickers} 
      />
      
      <VolumeChart data={data.volumeData} tickers={data.tickers} />
    </div>
  );
}

export default Results;

