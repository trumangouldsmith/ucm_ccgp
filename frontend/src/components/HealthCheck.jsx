import { useState, useEffect } from 'react';
import { checkHealth } from '../services/api';
import './HealthCheck.css';

function HealthCheck() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkApiHealth = async () => {
      try {
        const data = await checkHealth();
        setHealth(data);
        setLoading(false);
      } catch (err) {
        setHealth({ status: 'error', message: err.message });
        setLoading(false);
      }
    };

    checkApiHealth();
  }, []);

  if (loading) {
    return <div className="health-check loading">Checking API...</div>;
  }

  return (
    <div className={`health-check ${health.status === 'healthy' ? 'healthy' : 'error'}`}>
      {health.status === 'healthy' ? (
        <>✓ API Connected</>
      ) : (
        <>⚠ API Unavailable</>
      )}
    </div>
  );
}

export default HealthCheck;

