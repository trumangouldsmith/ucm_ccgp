import './CorrelationMatrix.css';

function CorrelationMatrix({ correlationMatrix, tickers }) {
  if (!correlationMatrix || tickers.length < 2) {
    return null;
  }
  
  const getCorrelationColor = (value) => {
    if (value >= 0.7) return 'high-positive';
    if (value >= 0.3) return 'moderate-positive';
    if (value >= -0.3) return 'low';
    if (value >= -0.7) return 'moderate-negative';
    return 'high-negative';
  };
  
  return (
    <div className="correlation-container">
      <h3>Correlation Matrix</h3>
      <div className="table-wrapper">
        <table className="correlation-table">
          <thead>
            <tr>
              <th></th>
              {tickers.map(ticker => (
                <th key={ticker}>{ticker}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tickers.map(ticker1 => (
              <tr key={ticker1}>
                <td className="ticker-cell">{ticker1}</td>
                {tickers.map(ticker2 => {
                  const value = correlationMatrix[ticker1]?.[ticker2] ?? 0;
                  return (
                    <td
                      key={ticker2}
                      className={`correlation-cell ${getCorrelationColor(value)}`}
                    >
                      {value.toFixed(2)}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="correlation-legend">
        <div className="legend-item">
          <span className="legend-color high-positive"></span>
          <span>Strong Positive (&gt;0.7)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color moderate-positive"></span>
          <span>Moderate Positive (0.3-0.7)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color low"></span>
          <span>Low (-0.3-0.3)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color moderate-negative"></span>
          <span>Moderate Negative (-0.7--0.3)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color high-negative"></span>
          <span>Strong Negative (&lt;-0.7)</span>
        </div>
      </div>
    </div>
  );
}

export default CorrelationMatrix;

