import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

function Home() {
  const navigate = useNavigate();
  const [tickers, setTickers] = useState('');
  const [startDate, setStartDate] = useState('2025-11-01');
  const [endDate, setEndDate] = useState('2025-11-20');
  const [interval, setInterval] = useState('1d');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Parse tickers (comma-separated)
    const tickerList = tickers
      .split(',')
      .map(t => t.trim().toUpperCase())
      .filter(t => t.length > 0);
    
    if (tickerList.length === 0) {
      alert('Please enter at least one ticker symbol');
      return;
    }
    
    // Navigate to results page with query params
    const params = new URLSearchParams({
      tickers: tickerList.join(','),
      startDate,
      endDate,
      interval
    });
    
    navigate(`/results?${params.toString()}`);
  };

  return (
    <div className="home">
      <div className="hero">
        <h2>Compare Stock Performance</h2>
        <p>Analyze multiple stocks with metrics like returns, volatility, and correlations</p>
      </div>
      
      <div className="form-container">
        <form onSubmit={handleSubmit} className="analysis-form">
          <div className="form-group">
            <label htmlFor="tickers">Stock Tickers</label>
            <input
              id="tickers"
              type="text"
              value={tickers}
              onChange={(e) => setTickers(e.target.value)}
              placeholder="AAPL, GOOGL, MSFT"
              className="form-input"
              required
            />
            <small>Enter 1-10 ticker symbols, separated by commas</small>
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="startDate">Start Date</label>
              <input
                id="startDate"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="form-input"
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="endDate">End Date</label>
              <input
                id="endDate"
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="form-input"
                required
              />
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="interval">Interval</label>
            <select
              id="interval"
              value={interval}
              onChange={(e) => setInterval(e.target.value)}
              className="form-input"
            >
              <option value="5m">5 Minutes</option>
              <option value="15m">15 Minutes</option>
              <option value="30m">30 Minutes</option>
              <option value="1h">1 Hour</option>
              <option value="1d">Daily</option>
              <option value="1wk">Weekly</option>
              <option value="1mo">Monthly</option>
            </select>
          </div>
          
          <button type="submit" className="submit-button">
            Analyze Stocks
          </button>
        </form>
      </div>
    </div>
  );
}

export default Home;

