import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './PriceChart.css';

function PriceChart({ data, tickers }) {
  const colors = ['#2563eb', '#dc2626', '#16a34a', '#ea580c', '#7c3aed', '#db2777'];
  
  // Format date for display (show time if intraday)
  const formatXAxis = (dateStr) => {
    if (dateStr.includes(':')) {
      // Intraday - show time
      const date = new Date(dateStr);
      return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    }
    // Daily - show date
    return dateStr;
  };
  
  return (
    <div className="chart-container">
      <h3>Price Performance</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tickFormatter={formatXAxis}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis />
          <Tooltip 
            labelFormatter={formatXAxis}
          />
          <Legend />
          {tickers.map((ticker, index) => (
            <Line
              key={ticker}
              type="linear"
              dataKey={ticker}
              stroke={colors[index % colors.length]}
              strokeWidth={2}
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default PriceChart;

