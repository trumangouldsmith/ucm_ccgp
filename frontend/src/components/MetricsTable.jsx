import './MetricsTable.css';

function MetricsTable({ metrics }) {
  return (
    <div className="metrics-container">
      <h3>Performance Metrics</h3>
      <div className="table-wrapper">
        <table className="metrics-table">
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Total Return</th>
              <th>Volatility</th>
              <th>Avg Volume</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(metrics).map(([ticker, data]) => (
              <tr key={ticker}>
                <td className="ticker-cell">{ticker}</td>
                <td className={data.total_return >= 0 ? 'positive' : 'negative'}>
                  {data.total_return?.toFixed(2)}%
                </td>
                <td>{data.volatility?.toFixed(2)}%</td>
                <td>{data.average_volume?.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default MetricsTable;

