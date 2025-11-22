import axios from 'axios';

// API base URL - can be configured via environment variable
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error: No response received');
    } else {
      // Error setting up request
      console.error('Request Error:', error.message);
    }
    return Promise.reject(error);
  }
);

/**
 * Analyze stocks with given parameters
 * @param {Object} params - Analysis parameters
 * @param {string[]} params.tickers - Array of ticker symbols
 * @param {string} params.startDate - Start date (YYYY-MM-DD)
 * @param {string} params.endDate - End date (YYYY-MM-DD)
 * @param {string} params.interval - Data interval (1d, 1wk, 1mo)
 * @returns {Promise} Analysis results
 */
export const analyzeStocks = async ({ tickers, startDate, endDate, interval = '1d' }) => {
  try {
    const response = await apiClient.post('/api/analyze', {
      tickers,
      date_range: {
        start_date: startDate,
        end_date: endDate,
      },
      interval,
    });
    
    return response.data;
  } catch (error) {
    // Enhance error message
    if (error.response?.status === 503) {
      throw new Error('Backend service unavailable. Please try again later.');
    } else if (error.response?.status === 400) {
      throw new Error(error.response.data.detail || 'Invalid request parameters.');
    } else if (error.code === 'ECONNREFUSED') {
      throw new Error('Cannot connect to backend. Make sure the API server is running.');
    } else {
      throw new Error(error.response?.data?.detail || error.message || 'Failed to analyze stocks');
    }
  }
};

/**
 * Check API health
 * @returns {Promise} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('API health check failed');
  }
};

/**
 * Get cache statistics
 * @returns {Promise} Cache stats
 */
export const getCacheStats = async () => {
  try {
    const response = await apiClient.get('/api/cache/stats');
    return response.data;
  } catch (error) {
    throw new Error('Failed to get cache stats');
  }
};

/**
 * Clear cache
 * @returns {Promise} Clear result
 */
export const clearCache = async () => {
  try {
    const response = await apiClient.delete('/api/cache/clear');
    return response.data;
  } catch (error) {
    throw new Error('Failed to clear cache');
  }
};

export default apiClient;

