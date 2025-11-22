import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './VolumeChart.css';

function VolumeChart({ data, tickers }) {
  const colors = ['#2563eb', '#dc2626', '#16a34a', '#ea580c', '#7c3aed', '#db2777'];
  
  return (
    <div className="chart-container">
      <h3>Trading Volume</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          {tickers.map((ticker, index) => (
            <Bar
              key={ticker}
              dataKey={`${ticker}_volume`}
              fill={colors[index % colors.length]}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default VolumeChart;

