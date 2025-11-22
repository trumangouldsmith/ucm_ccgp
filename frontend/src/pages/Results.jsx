import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import './Results.css';

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
      
      // Placeholder - will connect to backend in next task
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setData({
          tickers,
          startDate,
          endDate,
          interval,
          message: 'Backend API integration pending (Task 10)'
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
      </div>
      
      <div className="placeholder">
        <p>{data?.message}</p>
        <p>Charts and metrics will be displayed here once backend is connected.</p>
      </div>
    </div>
  );
}

export default Results;

